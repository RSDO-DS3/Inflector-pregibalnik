# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import pickle
import tensorflow as tf

from lib.prepare_data import Data
import gc

class SloveneAccentuator:

    def __init__(self, env_pickle, models_directory):

        # Read variables necessary for calculations from given pickle file
        with open(env_pickle, 'rb') as env_file_file:
            environment = pickle.load(env_file_file)

            self.dictionary = environment['dictionary']
            self.max_word = environment['max_word']
            self.max_num_vowels = environment['max_num_vowels']
            self.vowels = environment['vowels']
            self.accented_vowels = environment['accented_vowels']
            self.feature_dictionary = environment['feature_dictionary']
            self.syllable_dictionary = environment['syllable_dictionary']

        # Load models from given directory
        self.data = Data('l', shuffle_all_inputs=False)
        self.letter_location_model, self.syllable_location_model, self.syllabled_letters_location_model = self.data.load_location_models(
            os.path.join(models_directory, 'word_accetuation/cnn_dictionary/v5_3/20_final_epoch.h5'),
            os.path.join(models_directory, 'word_accetuation/syllables/v3_3/20_final_epoch.h5'),
            os.path.join(models_directory, 'word_accetuation/syllabled_letters/v3_3/20_final_epoch.h5'))

        self.letter_location_co_model, self.syllable_location_co_model, self.syllabled_letters_location_co_model = self.data.load_location_models(
            os.path.join(models_directory, 'word_accetuation/cnn_dictionary/v5_2/20_final_epoch.h5'),
            os.path.join(models_directory, 'word_accetuation/syllables/v3_2/20_final_epoch.h5'),
            os.path.join(models_directory, 'word_accetuation/syllabled_letters/v3_2/20_final_epoch.h5'))

        self.letter_type_model, self.syllable_type_model, self.syllabled_letter_type_model = self.data.load_type_models(
            os.path.join(models_directory, 'accent_classification/letters/v3_1/20_final_epoch.h5'),
            os.path.join(models_directory, 'accent_classification/syllables/v2_1/20_final_epoch.h5'),
            os.path.join(models_directory, 'accent_classification/syllabled_letters/v2_1/20_final_epoch.h5'))

        self.letter_type_co_model, self.syllable_type_co_model, self.syllabled_letter_type_co_model = self.data.load_type_models(
            os.path.join(models_directory, 'accent_classification/letters/v3_0/20_final_epoch.h5'),
            os.path.join(models_directory, 'accent_classification/syllables/v2_0/20_final_epoch.h5'),
            os.path.join(models_directory, 'accent_classification/syllabled_letters/v2_0/20_final_epoch.h5'))

        # LOAD DATA CLASSES
        # location
        self.data_location_l = Data('l', shuffle_all_inputs=False, convert_multext=False)
        self.data_location_s = Data('s', shuffle_all_inputs=False, convert_multext=False)
        self.data_location_sl = Data('sl', shuffle_all_inputs=False, convert_multext=False)
        self.data_location_l_reverse = Data('l', shuffle_all_inputs=False, convert_multext=False, reverse_inputs=False)
        self.data_location_s_reverse = Data('s', shuffle_all_inputs=False, convert_multext=False, reverse_inputs=False)
        self.data_location_sl_reverse = Data('sl', shuffle_all_inputs=False, convert_multext=False, reverse_inputs=False)

        # type
        self.data_type_l = Data('l', shuffle_all_inputs=False, accent_classification=True, convert_multext=False)
        self.data_type_s = Data('s', shuffle_all_inputs=False, accent_classification=True, convert_multext=False)
        self.data_type_sl = Data('sl', shuffle_all_inputs=False, accent_classification=True, convert_multext=False)
        self.data_type_l_reverse = Data('l', shuffle_all_inputs=False, accent_classification=True, convert_multext=False, reverse_inputs=False)
        self.data_type_s_reverse = Data('s', shuffle_all_inputs=False, accent_classification=True, convert_multext=False, reverse_inputs=False)
        self.data_type_sl_reverse = Data('sl', shuffle_all_inputs=False, accent_classification=True, convert_multext=False, reverse_inputs=False)

    def convert_to_correct_accentuation(self, w):
        """The accentuate_word function returns placeholder accentuation symbols.
        They need to be replaced with actual accentuation symbols. """
        w = w.replace('ì', 'ê')
        w = w.replace('à', 'ŕ')
        w = w.replace('ä', 'à')
        w = w.replace('ë', 'è')
        w = w.replace('ě', 'ê')
        w = w.replace('î', 'ì')
        w = w.replace('ö', 'ò')
        w = w.replace('ü', 'ù')

        return w

    def get_accentuated_words(self, list_of_forms):
        # Format data for accentuate_word function; the format is the following: [['besedišči', '', 'Ncnpi', 'besedišči'], ]
        self.content = [[el[0], '', el[1], el[0]] for el in list_of_forms]

        # use environment variables and models to accentuate words
        # data = Data('l', shuffle_all_inputs=False)
        location_accented_words, accented_words = self.data.accentuate_word(self.content, self.letter_location_model,
                                                                            self.syllable_location_model,
                                                                            self.syllabled_letters_location_model,
                                                                            self.letter_location_co_model,
                                                                            self.syllable_location_co_model,
                                                                            self.syllabled_letters_location_co_model,
                                                                            self.letter_type_model, self.syllable_type_model,
                                                                            self.syllabled_letter_type_model,
                                                                            self.letter_type_co_model, self.syllable_type_co_model,
                                                                            self.syllabled_letter_type_co_model,
                                                                            self.dictionary, self.max_word, self.max_num_vowels, self.vowels,
                                                                            self.accented_vowels, self.feature_dictionary,
                                                                            self.syllable_dictionary,
                                                                            self.data_location_l,
                                                                            self.data_location_s,
                                                                            self.data_location_sl,
                                                                            self.data_location_l_reverse,
                                                                            self.data_location_s_reverse,
                                                                            self.data_location_sl_reverse,
                                                                            self.data_type_l,
                                                                            self.data_type_s,
                                                                            self.data_type_sl,
                                                                            self.data_type_l_reverse,
                                                                            self.data_type_s_reverse,
                                                                            self.data_type_sl_reverse
                                                                            )

        # Convert placeholder accentuation symbols to actual accentuation symbols
        accented_words_with_correct_accentuation_symbols = []
        for word in accented_words:
            accented_words_with_correct_accentuation_symbols.append(self.convert_to_correct_accentuation(word))

        final_list = []
        for index, form_msd in enumerate(list_of_forms):
            form, msd = form_msd
            accentuated_form = accented_words_with_correct_accentuation_symbols[index]
            final_list.append([form, msd, accentuated_form])

        tf.keras.backend.clear_session()
        gc.collect()
        return final_list
