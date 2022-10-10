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

    for idx, token in enumerate(spacy_output):
        spacy_words.append(spacy_output[idx].text)
        spacy_lemmas.append(spacy_output[idx].lemma_)
        spacy_pos.append(spacy_output[idx].pos_)
        spacy_tags.append(spacy_output[idx].tag_)
        spacy_deps.append(spacy_output[idx].dep_)
        spacy_stop.append(spacy_output[idx].is_stop)
        spacy_heads.append(spacy_output[idx].head)
        kids = []
        for x in spacy_output[idx].children:
            kids.append(x)
        spacy_children.append(kids)

    stative_verbs = ["be", "exist", "appear", "feel", "hear", "look", "see", "seem", "belong", "have", "own", "possess",
                     "like", "want", "wish", "prefer", "love", "hate", "make", "become", "meet"]
    satellites = ["across", "after", "along", "apart", "around", "about", "away", "back", "down", "under", "in", "into",
                  "off", "on", "onto", "out", "over", "above", "through", "to", "together", "below", "up"]
    likely_dates = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                    "November", "December"]
    path_verbs = ["enter", "exit", "return", "descend", "ascend", "rise", "cross", "follow", "depart", "arrive",
                  "advance", "leave", "circle", "pass", "approach", "near", "join", "separate"]
    path_reduplication = ["enter in", "enter into", "exit out", "return back", "ascend up", "rise up", "cross across",
                          "follow after", "advance forward", "leave away", "circle around", "pass by", "join together",
                          "separate apart", "attach on", "attach onto"]


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
        dep = spacy_deps[i]
        pos = spacy_pos[i]
        word = spacy_words[i]
        head = spacy_heads[i]
        head = f'{head}'

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
                                Adj_SF_examples.append(word_match + ' ' + word)
                                break
                            else:
                                x += 1


        if pos == "ADP" and word in satellites: #handles most satellites
            if head in satellites:
                SF_count += 1
                SF_examples.append(head + ' ' + word)
            elif head in list_o_verbs:
                if word in ["into", "onto"]:
                    if spacy_words[i+1] not in likely_dates and spacy_pos[i+1] != "NUM" and spacy_pos[i+1] != "PROPN":
                        for y in range(0, len(list_o_verbs)):
                            word_match = list_o_verbs[y]
                            word_lemma = list_o_vb_lemmas[y]
                            if word_match == head and word_lemma not in stative_verbs:
                                SF_count += 1
                                SF_examples.append(head + ' ' + word)
                                SF_lemma_examples.append(word_lemma + ' ' + word)
                                break

        if pos == "ADV" and word in satellites: #handles particles marked as adverbs as satellites
            if head in satellites:
                SF_count += 1
                SF_examples.append(head + ' ' + word)
            elif head in list_o_verbs:
                for y in range(0, len(list_o_verbs)):
                    word_match = list_o_verbs[y]
                    word_lemma = list_o_vb_lemmas[y]
                    if word_match == head and word_lemma not in stative_verbs:
                        SF_count += 1
                        SF_examples.append(head + ' ' + word)
                        SF_lemma_examples.append(word_lemma + ' ' + word)
                        break

    for i in list_o_vb_lemmas:
        idx = list_o_vb_lemmas.index(i)
        if i in path_verbs:
            VF_count += 1
            VF_examples.append(list_o_verbs[idx])

    for i in SF_lemma_examples:
        idx = SF_lemma_examples.index(i)
        if i in path_reduplication:
            SF_count -= 1
            PR_count += 1
            PR_examples.append(i)
            SF_examples.pop(idx)
            SF_lemma_examples.pop(idx)



    final_SF_string = '; '.join(SF_examples)
    final_PR_string = '; '.join(PR_examples)
    final_VF_string = '; '.join(VF_examples)
    final_adjective_SF_string = '; '.join(Adj_SF_examples)
    final_counts = {'Satellite-Framing': SF_count, 'Verb-Framing': VF_count, 'Path-Reduplication': PR_count}
    final_tokens = {'Satellite-Framing': final_SF_string, 'Verb-Framing': final_VF_string, 'Path-Reduplication': final_PR_string}
    final_changeofstate = {'Adjective Change of State Expressions': Adj_SF_Count, 'Adjective COS Examples': final_adjective_SF_string}
    filename_res = {'filename': filename}

    return {'filename': filename_res, 'counts': final_counts, 'tokens': final_tokens, 'change of state': final_changeofstate}

def write_header_and_data_to_file(header, data, output_filename):
    """

    :type header - a string.
    :param header: All the names of the variables from various types of analyzers
    :type data - list of strings.
    :param data: The scores of the variables from the various analyzers
    :param output_filename:
    :return:
    """
    assert Path(output_filename).parent.is_dir(), f'The directory: {Path(output_filename).parent.absolute()} does ' \
                                                  f'not exist. Cannot create output file. Please create the above ' \
                                                  f'directory, or choose another file location.'
    with open(output_filename, 'w', encoding='utf8', newline='') as output_file:
        output_file.write(header)
        for d in data:
            output_file.write(d)
    logger.info(f'{len(data)} lines of output written to: {output_filename}.')

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

def stringify_scores(scores):
    """
    Scores array is a list of dictionaries
    Format:
    [{'filename': filename, 'counts': event_counts, 'tokens': token_results},...]
    :param scores:
    :return:
    """
    string_scores = ''
    for sc in scores:
        for key in sc.keys():
            for v in sc[key].values():
                string_scores += f'{v},'
        string_scores += '\n'
    return string_scores

def write_header_and_data_to_file(header, data, output_filename):
    """
    Based on original function in Lu (2010, 2012), later modified in Spring & Johnson (2022)
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
        output_file.write(header)
        for d in data:
            output_file.write(d)
    logger.info(f'{len(data)} lines of output written to: {output_filename}.')

def build_header(scores):
    header = ''
    for key in scores[0]:
        for k in scores[0][key].keys():
            header += f'{k},'
    header += '\n'
    return header

def list_stringify_scores(scores):
    string_scores_list = []

    for sc in scores:
        string_score = ''
        for key in sc.keys():
            for v in sc[key].values():
                string_score += f'{v},'
        string_score += '\n'
        string_scores_list.append(string_score)
    return string_scores_list

def main(input_path):
    input_filepath = os.path.join(os.getcwd(), input_path)
    scores = []
    for fdx, filename in enumerate(os.listdir(input_filepath)):
        if filename.endswith('.txt'):
            result = process(os.path.join(input_filepath, filename), filename)
            scores.append(result)

    header = build_header(scores)
    string_scores = list_stringify_scores(scores)
    write_header_and_data_to_file(header, string_scores, os.path.join(os.getcwd(),
                                                                          f'./output/EC_Finder_{len(scores)}.csv'))


if __name__ == '__main__':
    main(sys.argv[1])