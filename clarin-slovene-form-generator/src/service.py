import os
from logging import getLogger
from typing import List
from fastapi import FastAPI, HTTPException
from form_generator import PatternPredictor, FormGenerator, PatternCodeRemapper
from model.FormOut import FormOut
from model.MsdEntryOut import MsdEntryOut
from model.OrthographyOut import OrthographyOut
from model.WordIn import WordIn
from mte6_translate import Mte6Translate

# Parameters
resources_directory = "../data/resources"
models_directory = "../data/models"
msd_dictionary = "../data/mte_6_dict_sl_en.tsv"

try:
    api_root_path = os.environ["API_ROOT_PATH"]
except KeyError as e:
    api_root_path = None

# Initialize components
logger = getLogger("uvicorn")
mte6Translate = Mte6Translate(msd_dictionary)
pattern_predictor = PatternPredictor(resources_directory, models_directory)
form_generator = FormGenerator(resources_directory)
pattern_code_remapper = PatternCodeRemapper(resources_directory)

# Create FastAPI application (this object is used by uvicorn web service to load application)
#app = FastAPI()
app = FastAPI(root_path=api_root_path, title="Form Generator API")



@app.post("/api/generate")
async def generate(word_in: WordIn):
    try:
        # Get lemma from input word
        lema_in = word_in.lema

        # Get msd from input word and convert it to slo
        if mte6Translate.get_msd_language(word_in.msd) == "sl":
            msd_in = word_in.msd
        else:
            msd_in = mte6Translate.msd_en_to_sl(word_in.msd)

        # Get pattern code from input word or calculate it if it is not given
        if word_in.patternCode is not None:
            pattern_code = word_in.patternCode
        else:
            pattern_code = pattern_predictor.predict_morphological_pattern(lemma=lema_in, msd=msd_in)

        # Generate forms based on pattern code
        pattern_dictionary = form_generator.generate_forms(pattern_code=pattern_code, lemma=lema_in)
        remapped_pattern_code = pattern_code_remapper.remap_pattern_code(pattern_code=pattern_code)

        # Create response
        response = []
        for msd, form_list in pattern_dictionary.items():
            forms = []
            for form in form_list:
                orthographies = []
                orthographies.append(OrthographyOut(text=form, morphologyPatterns=remapped_pattern_code))
                # Add more orthographies here if required

                # Add orthographies to current form
                forms.append(FormOut(orthographies=orthographies))

            # Add current form to msd entry
            response.append(MsdEntryOut(msd=msd, forms=forms))

        # Return whole response
        return response

    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Caught unexpected error while processing following request data: ({requestObject}).".format(requestObject=word_in))


@app.post("/api/generate-all")
async def generate_all(words_in: List[WordIn]):
    # Generate forms for all received words, but do not await the results
    async_generate_tasks = [generate(word_in) for word_in in words_in]

    # Await all tasks and map results to response dto
    return [await task for task in async_generate_tasks]
