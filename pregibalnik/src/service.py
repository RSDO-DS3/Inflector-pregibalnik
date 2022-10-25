import os
from logging import getLogger
from typing import List
from fastapi import FastAPI, HTTPException
import requests

from model.AccentuationOut import AccentuationOut
from model.FormOut import FormOut
from model.MsdEntryOut import MsdEntryOut
from model.OrthographyOut import OrthographyOut
from model.PronunciationFormOut import PronunciationFormOut
from model.PronunciationOut import PronunciationOut
from model.WordIn import WordIn

logger = getLogger("uvicorn")

# Parameters
try:
    form_generator_url = os.environ["FORM_GENERATOR_URL"]
    accentuator_url = os.environ["ACCENTUATOR_URL"]
    g2p_converter_url = os.environ["G2P_CONVERTER_URL"]
except KeyError as e:
    raise Exception("Missing environment variable {}".format(e.args[0]))

# Create FastAPI application (this object is used by uvicorn web service to load application)
app = FastAPI()


@app.post("/api/process")
async def process(word_in: WordIn):
    logger.debug("Processing request: {}".format(word_in))

    # Call form generator to create all word forms
    word_forms_response = requests.post(
        form_generator_url + "/api/generate",
        json={
            "lema": word_in.lema,
            "msd": word_in.msd,
            "patternCode": word_in.patternCode
        }
    )

    # Check response status
    if word_forms_response.status_code != 200:
        raise HTTPException(500, "Received unexpected response code from 'form-generator'. Expected: {expected}; Received: {received}; Message: {message}".format(
            expected=200,
            received=word_forms_response.status_code,
            message=word_forms_response.json()
        ))
    word_forms = word_forms_response.json()

    # Create request object for accentuator
    orthographies_to_accentuate = []
    for msd_entry in word_forms:
        for form in msd_entry["forms"]:
            for orthography in form["orthographies"]:
                orthographies_to_accentuate.append({
                    "text": orthography["text"],
                    "msd": msd_entry["msd"]
                })

    # Call accentuator with a list of orthographies
    accentuation_response = requests.post(
        accentuator_url + "/api/accentuate-all",
        json=orthographies_to_accentuate
    )

    # Check response status
    if accentuation_response.status_code != 200:
        raise HTTPException(500, "Received unexpected response code from 'accentuator'. Expected: {expected}; Received: {received}; Message: {message}".format(
            expected=200,
            received=accentuation_response.status_code,
            message=accentuation_response.json()
        ))
    accentuated_orthographies = accentuation_response.json()

    # Match request objects with returned objects by indexes
    current_index = 0
    msd_entries_out = []
    for msd_entry in word_forms:
        forms_out = []
        for form in msd_entry["forms"]:
            orthographies_out = []
            for orthography in form["orthographies"]:

                accentuation = accentuated_orthographies[current_index]
                current_index += 1

                # Call IPA/SAMPA converter for each accentuation
                pronunciations_response = requests.post(
                    g2p_converter_url + "/api/convert",
                    json={
                        "text": accentuation["accText"],
                        "msd": msd_entry["msd"],
                        "morphologyPattern": orthography["morphologyPatterns"]
                    }
                )

                # Check response status
                if pronunciations_response.status_code != 200:
                    raise HTTPException(500, "Received unexpected response code from 'g2p converter'. Expected: {expected}; Received: {received}; Message: {message}".format(
                        expected=200,
                        received=pronunciations_response.status_code,
                        message=pronunciations_response.json()
                    ))

                # Process response body
                pronunciation_forms_out = []
                for pronunciation in pronunciations_response.json():
                    pronunciation_forms_out.append(PronunciationFormOut(
                        text=pronunciation["text"],
                        script=pronunciation["script"]
                    ))

                accentuations_out = [AccentuationOut(
                    text=accentuation["accText"],
                    type="dynamic",
                    pronunciations=[PronunciationOut(forms=pronunciation_forms_out)]
                )]

                orthography_out = OrthographyOut(
                    text=orthography["text"],
                    morphologyPatterns=orthography["morphologyPatterns"],
                    accentuations=accentuations_out
                )
                orthographies_out.append(orthography_out)

            forms_out.append(FormOut(orthographies=orthographies_out))
            msd_entries_out.append(MsdEntryOut(msd=msd_entry["msd"], forms=forms_out))

    return msd_entries_out


@app.post("/api/process-all")
async def process_all(words_in: List[WordIn]):
    # process all requests
    async_process_tasks = [process(word_in) for word_in in words_in]

    # Await all tasks and map results to response dto
    return [await task for task in async_process_tasks]
