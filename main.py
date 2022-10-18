import os
import sys
import spacy
from pathlib import Path
import logging
import csv

logger = logging.getLogger('EV_Finder')

def safe_division(x, y):
    """
    Safely divide numbers; i.e., give a score of 0 if numerator or denominator is 0
    :param x:
    :param y:
    :return:
    """
    if float(x) == 0 or float(y) == 0:
        return 0
    return float(x) / float(y)

def get_events(filename, spacy_output):
    """
    Splits SpaCy into relevant elements, makes counts of verb- and satellite-framing based on lists.
    Also pulls the specific parts from the text for user checking.
    :param filename: passes in the file name
    :param spacy_output: the tokenized information provided by SpaCy
    :return:
    """
    spacy_words = []
    spacy_lemmas = []
    spacy_pos = []
    spacy_tags = []
    spacy_deps = []
    spacy_stop = []
    spacy_heads = []
    spacy_children = []
    spacy_sentences = []

    for idx, token in enumerate(spacy_output):
        spacy_words.append(spacy_output[idx].text)
        spacy_lemmas.append(spacy_output[idx].lemma_)
        spacy_pos.append(spacy_output[idx].pos_)
        spacy_tags.append(spacy_output[idx].tag_)
        spacy_deps.append(spacy_output[idx].dep_)
        spacy_stop.append(spacy_output[idx].is_stop)
        spacy_heads.append(spacy_output[idx].head)
        spacy_sentences.append(spacy_output[idx].sent)
        kids = []
        for x in spacy_output[idx].children:
            kids.append(x)
        spacy_children.append(kids)

    stative_verbs = ["be", "exist", "appear", "feel", "hear", "look", "see", "seem", "belong", "have", "own", "possess",
                     "like", "live", "want", "wish", "prefer", "love", "hate", "make", "become", "meet", "depend",
                     "fit", "touch", "matter", "lay", "lie", "find"]
    satellites = ["aboard", "about", "above", "across", "after", "against", "ahead", "along", "amid", "among",
                  "amongst", "around", "aside", "away", "back", "before", "behind", "below", "beneath", "beside",
                  "between", "beyond", "down", "from", "in", "inside", "into", "near", "off", "on", "onto", "opposite",
                  "out", "outside", "over", "past", "round", "through", "to", "toward", "towards", "together", "under",
                  "underneath", "up", "upon"]
    likely_dates = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                    "November", "December", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
                    "Sunday"]
    path_verbs = ["enter", "exit", "return", "descend", "ascend", "rise", "cross", "follow", "depart", "arrive",
                  "advance", "leave", "circle", "pass", "approach", "near", "join", "separate", "proceed"]
    path_reduplication = ["enter in", "enter into", "exit out", "return back", "ascend up", "rise up", "cross across",
                          "follow after", "advance forward", "leave away", "circle around", "pass by", "join together",
                          "separate apart", "attach on", "attach onto"]
    exceptions = ["punch on", "light on", "use to", "take to", "talk about"]

    SF_count = 0
    Adj_SF_Count = 0
    VF_count = 0
    PR_count = 0
    Adj_SF_examples = []
    SF_examples = []
    SF_lemma_examples = []
    PR_examples = []
    VF_examples = []
    list_o_verbs = []
    list_o_vb_lemmas = []

    for i in range(0, len(spacy_pos)):
        pos = spacy_pos[i]
        verb_lemma = spacy_lemmas[i]
        verb = spacy_words[i]
        if pos == "VERB":
            list_o_verbs.append(verb)
            list_o_vb_lemmas.append(verb_lemma)

    for i in range(0, len(spacy_deps)):
        pos = spacy_pos[i]
        word = spacy_words[i]
        head = spacy_heads[i]
        head = f'{head}'
        the_sentence = spacy_sentences[i]
        the_sentence = f"{the_sentence}"
        the_sentence = the_sentence.rstrip()
        the_lemma = spacy_lemmas[i]

        if pos == "ADJ": #handles adjectives as satellites
            if head in list_o_verbs:
                for y in range(0, len(list_o_verbs)):
                    word_match = list_o_verbs[y]
                    word_lemma = list_o_vb_lemmas[y]
                    if word_match == head and word_lemma not in stative_verbs:
                        x = 0
                        while x < i:
                            double_match = spacy_words[x]
                            if head == double_match:
                                Adj_SF_Count += 1
                                Adj_SF_examples.append(word_match + ' ' + word + ' ("' + the_sentence + '")')
                                break
                            else:
                                x += 1


        if pos == "ADP" and word in satellites: #handles most satellites
            if head in satellites:
                SF_count += 1
                SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
            elif head in list_o_verbs:
                if word in ["into", "onto", "on"]:
                    if spacy_words[i+1] not in likely_dates and spacy_pos[i+1] != "NUM" and spacy_words[i+2] not in ["morning", "evening", "night"] and spacy_pos[i+1] != "PROPN":
                        for y in range(0, len(list_o_verbs)):
                            word_match = list_o_verbs[y]
                            word_lemma = list_o_vb_lemmas[y]
                            if word_match == head and word_lemma not in stative_verbs:
                                if (word_lemma + ' ' + word) in path_reduplication:
                                    PR_count += 1
                                    PR_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                                elif word_lemma not in path_verbs and (word_lemma + ' ' + word) not in exceptions:
                                    SF_count += 1
                                    SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                                    SF_lemma_examples.append(word_lemma + ' ' + word)
                                    break
                elif spacy_words[i+1] not in likely_dates and spacy_pos[i+1] != "NUM" and spacy_words[i+2] not in ["morning", "evening", "night"] and spacy_pos[i+1] != "PROPN":
                    for y in range(0, len(list_o_verbs)):
                        word_match = list_o_verbs[y]
                        word_lemma = list_o_vb_lemmas[y]
                        if word_match == head and word_lemma not in stative_verbs:
                            if (word_lemma + ' ' + word) in path_reduplication:
                                PR_count += 1
                                PR_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                            elif word_lemma not in path_verbs and (word_lemma + ' ' + word) not in exceptions:
                                SF_count += 1
                                SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                                SF_lemma_examples.append(word_lemma + ' ' + word)
                                break

        if pos == "ADV" and word in satellites: #handles particles marked as adverbs as satellites
            if head in satellites:
                SF_count += 1
                SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
            elif head in list_o_verbs:
                for y in range(0, len(list_o_verbs)):
                    word_match = list_o_verbs[y]
                    word_lemma = list_o_vb_lemmas[y]
                    if word_match == head and word_lemma not in stative_verbs:
                        if (word_lemma + ' ' + word) in path_reduplication:
                            PR_count += 1
                            PR_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                        elif word_lemma not in path_verbs and (word_lemma + ' ' + word) not in exceptions:
                            SF_count += 1
                            SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                            SF_lemma_examples.append(word_lemma + ' ' + word)
                            break

        if pos == "VERB" and the_lemma in path_verbs:
            if (the_lemma + ' ' + word) not in path_reduplication:
                VF_count += 1
                VF_examples.append(word + ' ("' + the_sentence + '")')


    final_SF_string = "\n".join(SF_examples)
    final_PR_string = '\n'.join(PR_examples)
    final_VF_string = '\n'.join(VF_examples)
    final_adjective_SF_string = '\n'.join(Adj_SF_examples)
    final_counts = {'Satellite-Framing': SF_count, 'Verb-Framing': VF_count, 'Path-Reduplication': PR_count}
    final_tokens = {'Satellite-Framing': final_SF_string, 'Verb-Framing': final_VF_string, 'Path-Reduplication': final_PR_string}
    final_changeofstate = {'Adjective Change of State Expressions': Adj_SF_Count, 'Adjective COS Examples': final_adjective_SF_string}
    filename_res = {'filename': filename}
    #return {"filename": filename_res, "counts": final_counts, "tokens": final_tokens, "change of state": final_changeofstate}
    return [filename, SF_count, final_SF_string, VF_count, final_VF_string, PR_count, final_PR_string, Adj_SF_Count, final_adjective_SF_string]

def read_input_text(filename):
    """
    Takes file name with encoding as utf8
    If the file encounters non-utf8 characters, it returns an error
    :param filename:
    :return:
    """
    text_lines = ""
    try:
        with open(filename, 'r', encoding='utf8') as f:
            text_lines = f.readlines()
            logger.info(f'Read file: {filename} - {len(text_lines)} lines read.')
    except:
        text_lines = 'unrecognized characters in file - unable to process'
        logger.warning(f'Filename:{filename} could not be read. Returning empty read-lines.')

    finally:
        return text_lines

def process(file_path: str, filename):
    """
    Simply preps files by sending files to get read and handling encoding errors.
    Also gets singular analysis from SpaCy, then sends to analyzer.
    :param file_path: path of file
    :param filename: actual file name
    :return:
    """
    text_lines = read_input_text(file_path)
    input_text = ''.join(text_lines)

    if input_text == 'unrecognized characters in file - unable to process':
        results = get_events(filename, "")
        return results
    else:
        nlp = spacy.load("en_core_web_lg")
        analysis = nlp(input_text)
        results = get_events(filename, analysis)
        return results

def write_data_to_file(data, output_filename):
    """
    :type header - a string.
    :param header:
    :type data - list of strings.
    :param data:
    :param output_filename:
    :return:
    """
    assert Path(output_filename).parent.is_dir(), f'The directory: {Path(output_filename).parent.absolute()} does ' \
                                                  f'not exist. Cannot create output file. Please create the above ' \
                                                  f'directory, or choose another file location.'
    with open(output_filename, 'w', encoding='utf8', newline='') as output_file:
        for d in data:
            output_file.write(d)
    logger.info(f'{len(data)} lines of output written to: {output_filename}.')

def list_stringify_scores(scores):
    string_scores_list = []

    for sc in scores:
        string_score = ""
        string_score += "Filename: " + sc[0] + "\n" + "\n"
        string_score += "Satellite-Framing Count: " + f"{sc[1]}" + "\n" + "\n"
        string_score += "Satellite-Framing Examples: " + "\n" + sc[2] + "\n" + "\n"
        string_score += "Verb-Framing Count: " + f"{sc[3]}" + "\n" + "\n"
        string_score += "Verb-Framing Examples: " + "\n" + sc[4] + "\n" + "\n"
        string_score += "Path Reduplication Count: " + f"{sc[5]}" + "\n" + "\n"
        string_score += "Path Reduplication Examples: " + "\n" + sc[6] + "\n" + "\n"
        string_score += "Adjectives as Satellites Count: " + f"{sc[7]}" + "\n" + "\n"
        string_score += "Adjectives as Satellites Examples: " + "\n" + sc[8] + "\n"
        string_score += "\n" + "\n" + "\n"
        string_scores_list.append(string_score)
    return string_scores_list

def main(input_path):
    input_filepath = os.path.join(os.getcwd(), input_path)
    scores = []
    for fdx, filename in enumerate(os.listdir(input_filepath)):
        if filename.endswith('.txt'):
            result = process(os.path.join(input_filepath, filename), filename)
            scores.append(result)

    string_scores = list_stringify_scores(scores)
    write_data_to_file(string_scores, os.path.join(os.getcwd(), f'./output/EC_Finder_{len(scores)}.txt'))


if __name__ == '__main__':
    main(sys.argv[1])