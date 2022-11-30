from logging import getLogger
from typing import List
from fastapi import FastAPI, HTTPException
from accentuate import SloveneAccentuator
from model.AccentuatedFormOut import AccentuatedFormOut
from model.FormIn import FormIn
from mte6_translate import Mte6Translate

# Parameters
env_pickle = "../data/environment.pkl"
models_directory = "../data/cnn"
msd_dictionary = "../data/mte_6_dict_sl_en.tsv"

# Initialize components
logger = getLogger("uvicorn")
mte6Translate = Mte6Translate(msd_dictionary)
sloveneAccentuator = SloveneAccentuator(env_pickle, models_directory)

# Create FastAPI application (this object is used by uvicorn web service to load application)
app = FastAPI()


@app.post("/api/accentuate")
async def accentuate(form_in: FormIn):
    # Forward the response to other function that accepts a list because accentuator only work with list inputs
    return (await accentuate_all([form_in]))[0]


@app.post("/api/accentuate-all")
async def accentuate_all(forms_in: List[FormIn]):
    try:
        # Convert input dto to the target object expected by accentuator
        forms_to_accentuate = []
        for form_in in forms_in:
            # Get msd from input word and convert it to slo
            if mte6Translate.get_msd_language(form_in.msd) == "en":
                msd_in = form_in.msd
            else:
                msd_in = mte6Translate.msd_sl_to_en(form_in.msd)

            # Append to list
            forms_to_accentuate.append([form_in.text, msd_in])

        # BUGFIX accentuator crashes if there are less than 3 input elements.
        # Therefore, add dummy elements to the input and remove them before returning the response
        dummy_forms = 0
        while len(forms_to_accentuate) < 3:
            forms_to_accentuate.append(["Dummy", "Somei"])
            dummy_forms += 1

        # Accentuate list of received word forms
        try:
            accentuated_forms = sloveneAccentuator.get_accentuated_words(forms_to_accentuate)
        except:
            # If the accentuator encounters an error when accentuating the list of words, it returns unaccentuated words instead to avoid crashing
            accentuated_forms = [[sublist[0], sublist[1], sublist[0]] for sublist in forms_to_accentuate]

        # Remove dummy forms
        if 0 < dummy_forms:
            accentuated_forms = accentuated_forms[:len(accentuated_forms) - dummy_forms]

        # Map to output dto and return
        return [map_to_accentuated_form_out(accentuated_form) for accentuated_form in accentuated_forms]

    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Caught unexpected error while processing following request data: ({requestObject}).".format(requestObject=forms_in))


def map_to_accentuated_form_out(accentuated_form):
    return AccentuatedFormOut(
        accText=accentuated_form[2]
    )
