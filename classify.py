# classify.py
# Language classification ported to Python
# (c) Alex King, 12/19/2014

from __future__ import division # For non-integer division
import sys # For file IO
import os  # For directory operations
import math # For sqrt and bit vector calculation

import urllib # For web page functionality

############################## MODEL GENERATION ################################

# str_to_trigrams : string -> list
# creates python list of trigrams from string
def str_to_trigrams(string):
        list = []
        for x in range(0, len(string) - 2): # For every group of three letters
                list.append(string[x] + string[x + 1] + string[x + 2])
        return list

# add_list_to_dict : list, dictionary -> dictionary
# Adds specified list of trigrams to occurrence dictionary
def add_list_to_dict(list, dict):
        for x in list: # For each trigram in the list, add it or increment count
                if dict.has_key(x):
                        dict[x] += 1
                else:
                        dict[x] = 1
        return dict

# single_lang_model : string -> tuple (langname, dictionary)
# creates tuple with specified language name and model (if langname exists)
def single_lang_model(mode, langname):
        dict = {}
        path = "./" + mode + "/" + langname + "/" # construct folder path
        for file in os.listdir(path):
                fullpath = path + file
                trigrams = str_to_trigrams((open(fullpath)).read())
                add_list_to_dict(trigrams, dict)
        tuple = (langname, dict);
        return tuple

# build_all_models : string -> list_of_tuples [(langname, dictionary)]
# returns list of all model tuples containing language name and model
# based on mode inputted, lang or subject
def build_all_models(mode):
        model_list = []
        dir = "./" + mode + "/"
        for lang in os.listdir(dir):
                model_list.append(single_lang_model(mode, lang))
        return model_list

# make_file_model : filename -> dictionary
# makes trigram occurrence model from specified file (if it exists)
def make_file_model(filename):
        if (filename.startswith("http://")):
                sock = urllib.urlopen(filename)
                trigrams = str_to_trigrams((sock.read()))
                sock.close()
        else:
                trigrams = str_to_trigrams((open(filename)).read())
        dict = add_list_to_dict(trigrams, {})
        return dict

############################ CLASSIFICATION ####################################

# nearest_model : dictionary list_of_tuples -> string
# returns name of language with highest similarity score given file and models
def nearest_model(file_model, model_list):
        score_list = [] # empty score list to start
        for model in model_list: # Compute each similarity score as list
                score_list.append(bit_vector_sim(file_model, model))
        # find the index of the highest score, use to index the model list

        # Verbose output -- uncomment to see scores of each language
        # for score in score_list:
        #         sys.stdout.write(model_list[score_list.index(score)][0])
        #         sys.stdout.write(": ")
        #         print score # score

        return model_list[score_list.index(max(score_list))][0]

# bit_vector_sim : dictionary dictionary -> number
# returns bit vector similarity score given two dictionaries; scores range 0-1
def bit_vector_sim(model1, model2):
        count = 0
        for key in model1.keys(): # map over every key
                if model2[1].has_key(key): 
                        count += 1
        return count / ((math.sqrt(len(model1))) * (math.sqrt(len(model2[1]))))

# main
def main():
        if len(sys.argv) != 3:
                sys.stdout.write("Usage: python classify.py [--lang|--subject]") 
                print " [file.txt|http://webpage.com]"
                sys.exit(1)
        mode = (str(sys.argv[1]))[2:]
        if ((mode != "lang") and (mode != "subject")):
                print "Unrecognized option. Use --lang for natural language," 
                print "or --subject for academic subject in English."
                sys.exit(1)
        file_model = make_file_model(str(sys.argv[2])) # Make model for file
        model_list = build_all_models(mode) # Make all language models
        print nearest_model(file_model, model_list) # print language name
main() # run main