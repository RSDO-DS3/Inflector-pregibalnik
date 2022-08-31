from logging import getLogger
from typing import List
from SloveneG2P import SloveneG2P
from fastapi import FastAPI, HTTPException
from model.AccentuatedFormIn import AccentuatedFormIn
from model.PronunciationOut import PronunciationOut

# Parameters
data_directory = "../data/dict"

# Initialize components
logger = getLogger("uvicorn")
ipa_converter = SloveneG2P(data_directory=data_directory, phoneme_set_option="ipa_symbol", representation_option="cjvt_ipa_detailed_representation", output_option="phoneme_string")
sampa_converter = SloveneG2P(data_directory=data_directory, phoneme_set_option="sampa_symbol", representation_option="cjvt_sampa_detailed_representation", output_option="phoneme_string")

# Create FastAPI application (this object is used by uvicorn web service to load application)
app = FastAPI()


@app.post("/api/convert")
async def convert(accentuated_form_in: AccentuatedFormIn):
    try:

        # Create a list that will hold all created pronunciations
        pronunciations_list_out = []

        # Create IPA pronunciation and add it to the list
        pronunciations_list_out.append(PronunciationOut(
            text=ipa_converter.convert_to_phonetic_transcription(word=accentuated_form_in.text, msd_sl=accentuated_form_in.msd, morphological_pattern_code=accentuated_form_in.morphologyPattern),
            script="IPA"
        ))

        # Create SAMPA pronunciation and add it to the list
        pronunciations_list_out.append(PronunciationOut(
            text=sampa_converter.convert_to_phonetic_transcription(word=accentuated_form_in.text, msd_sl=accentuated_form_in.msd, morphological_pattern_code=accentuated_form_in.morphologyPattern),
            script="SAMPA"
        ))

        # Return list of all pronunciations
        return pronunciations_list_out

    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Caught unexpected error while processing following request data: ({requestObject}).".format(requestObject=accentuated_form_in))


@app.post("/api/convert-all")
async def convert_all(accentuated_words_in: List[AccentuatedFormIn]):
    # Convert each given form to pronunciation, but do not await the response
    async_convert_tasks = [convert(accentuated_word_in) for accentuated_word_in in accentuated_words_in]

    # Await all tasks and map results to response dto
    return [await task for task in async_convert_tasks]
