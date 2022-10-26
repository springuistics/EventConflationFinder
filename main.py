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

def load_word_list(filename):
    the_filepath = os.path.join(os.getcwd(), filename)

    with open(the_filepath, 'r', encoding='utf8') as f:
        word_list = f.read().split('\n')
    unique_words = list(dict.fromkeys(word_list))
    clean_words = []
    for word in unique_words:
        clean_words.append(word.strip().lower())
    if '' in clean_words:
        clean_words.remove('')  # remove any empty strings.
    return clean_words

def get_events_j(filename, spacy_output):
    """
    Splits SpaCy into relevant elements for Japanese, makes counts of verb- and satellite-framing based on lists.
    :param filename:
    :param spacy_output:
    :return:
    """

    spacy_words = []
    spacy_lemmas = []
    spacy_pos = []
    spacy_deps = []
    spacy_heads = []
    spacy_children = []
    spacy_sentences = []

    for idx, token in enumerate(spacy_output):
        spacy_words.append(spacy_output[idx].text)
        spacy_lemmas.append(spacy_output[idx].lemma_)
        spacy_pos.append(spacy_output[idx].pos_)
        spacy_deps.append(spacy_output[idx].dep_)
        spacy_heads.append(spacy_output[idx].head)
        spacy_sentences.append(spacy_output[idx].sent)
        kids = []
        for x in spacy_output[idx].children:
            kids.append(x)
        spacy_children.append(kids)

    stative_verbs = ["です"]

    satellites = ["まで"]

    path_verbs = ["渡る"]

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

        if pos == "VERB" and the_lemma in path_verbs:
            VF_count += 1
            VF_examples.append(word + ' ("' + the_sentence + '")')

        if pos == "PART" and word in satellites:
            SF_count += 1
            SF_lemma_examples.append(word + head)
            SF_examples.append(word + head + ' ("' + the_sentence + '")')




    final_SF_string = "\n".join(SF_examples)
    final_PR_string = '\n'.join(PR_examples)
    final_VF_string = '\n'.join(VF_examples)
    final_adjective_SF_string = '\n'.join(Adj_SF_examples)
    return [filename, SF_count, final_SF_string, VF_count, final_VF_string, PR_count, final_PR_string, Adj_SF_Count, final_adjective_SF_string]


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
    likely_dates = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                    "November", "December", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
                    "Sunday"]
    mm_verbs = load_word_list("word_lists\clear_manner_of_motion_vbs.txt")
    bare_verbs = ['go', 'come', 'get', 'move', 'travel']
    path_verbs = load_word_list("word_lists\path_verbs.txt")
    path_reduplication = load_word_list("word_lists\path_reduplication.txt")
    counts_as_motion = ['sit down', 'stand up', 'lay down']
    doesnt_count_double_sat = ['away from', 'off of']
    exceptions = ["punch on", "light on", "use to", "take to", "talk about"]
    satellites = load_word_list("word_lists\satellites.txt")
    mchange_verbs = load_word_list("word_lists\manner_of_change_verbs.txt")
    vchange_verbs = load_word_list("word_lists\path_of_change_verbs.txt")
    change_redup = load_word_list("word_lists\change_reduplication.txt")
    change_redup2 = load_word_list("word_lists\change_redup_multiword.txt")

    Motion_SF_count = 0
    Change_SF_Count = 0
    Motion_VF_count = 0
    Change_VF_Count = 0
    Motion_PR_count = 0
    Change_PR_count = 0
    Unsure_SF_count = 0
    Change_SF_examples = []
    Change_SF_lemma_examples = []
    Change_VF_examples = []
    Change_PR_examples = []
    SF_examples = []
    SF_lemma_examples = []
    PR_examples = []
    VF_examples = []
    Unsure_SF_examples = []
    Unsure_SF_lemma_examples = []

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
                    if word_match == head and word_lemma in mchange_verbs and (word_lemma + ' ' + word) in change_redup:
                        x = 0
                        while x < i:
                            double_match = spacy_words[x]
                            if head == double_match:
                                Change_PR_count += 1
                                Change_PR_examples.append(word_match + ' ' + word + ' ("' + the_sentence + '")')
                                break
                            else:
                                x += 1
                        break
                    elif word_match == head and word_lemma in mchange_verbs or word_lemma in bare_verbs:
                        x = 0
                        while x < i:
                            double_match = spacy_words[x]
                            if head == double_match:
                                Change_SF_Count += 1
                                Change_SF_examples.append(word_match + ' ' + word + ' ("' + the_sentence + '")')
                                Change_SF_lemma_examples.append(word_lemma + ' ' + word)
                                break
                            else:
                                x += 1
                        break
                    elif word_match == head and word_lemma not in stative_verbs:
                        x = 0
                        while x < i:
                            double_match = spacy_words[x]
                            if head == double_match:
                                Unsure_SF_count += 1
                                Unsure_SF_examples.append(word_match + ' ' + word + ' ("' + the_sentence + '")')
                                Unsure_SF_lemma_examples.append(word_lemma + ' ' + word)
                                break
                            else:
                                x += 1
                        break


        if pos == "ADP" and word in satellites: #handles most satellites
            if head in satellites and (head + ' ' + word) not in doesnt_count_double_sat:
                Motion_SF_count += 1
                SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
            elif head in list_o_verbs:
                if word in ["into", "onto", "on"]:
                    if spacy_words[i+1] not in likely_dates and spacy_pos[i+1] != "NUM" and spacy_words[i+2] not in ["morning", "evening", "night"] and spacy_pos[i+1] != "PROPN":
                        for y in range(0, len(list_o_verbs)):
                            word_match = list_o_verbs[y]
                            word_lemma = list_o_vb_lemmas[y]
                            if word_match == head and (word_lemma + ' ' + word) in path_reduplication:
                                Motion_PR_count += 1
                                PR_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                                break
                            elif word_match == head and (word_lemma + ' ' + word) in counts_as_motion:
                                Motion_SF_count += 1
                                SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                                SF_lemma_examples.append(word_lemma + ' ' + word)
                                break
                            elif word_match == head and word_lemma in mm_verbs and (word_lemma + ' ' + word) not in exceptions:
                                Motion_SF_count += 1
                                SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                                SF_lemma_examples.append(word_lemma + ' ' + word)
                                break
                            elif word_match == head and word_lemma in mchange_verbs and (word_lemma + ' ' + word) in change_redup:
                                Change_PR_count += 1
                                Change_PR_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                                break
                            elif word_match == head and word_lemma in mchange_verbs and word in ["into"]:
                                if (word_lemma + ' ' + word + ' ' + spacy_words[i+1]) in change_redup2:
                                    Change_PR_count += 1
                                    Change_PR_examples.append(head + ' ' + word + ' ' + spacy_words[i+1] + ' ("' + the_sentence + '")')
                                    break
                            elif word_match == head and word_lemma in mchange_verbs and (word_lemma + ' ' + word) not in exceptions:
                                Change_SF_Count += 1
                                Change_SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                                Change_SF_lemma_examples.append(word_lemma + ' ' + word)
                                break
                            elif word_match == head and word_lemma not in stative_verbs and (word_lemma + ' ' + word) not in exceptions:
                                Unsure_SF_count += 1
                                Unsure_SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                                Unsure_SF_lemma_examples.append(word_lemma + ' ' + word)
                                break

                elif spacy_words[i+1] not in likely_dates and spacy_pos[i+1] != "NUM" and spacy_words[i+2] not in ["morning", "evening", "night"] and spacy_pos[i+1] != "PROPN":
                    for y in range(0, len(list_o_verbs)):
                        word_match = list_o_verbs[y]
                        word_lemma = list_o_vb_lemmas[y]
                        if word_match == head and (word_lemma + ' ' + word) in path_reduplication:
                            Motion_PR_count += 1
                            PR_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                            break
                        elif word_match == head and (word_lemma + ' ' + word) in counts_as_motion:
                            Motion_SF_count += 1
                            SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                            SF_lemma_examples.append(word_lemma + ' ' + word)
                            break
                        elif word_match == head and word_lemma in mm_verbs and (word_lemma + ' ' + word) not in exceptions:
                            Motion_SF_count += 1
                            SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                            SF_lemma_examples.append(word_lemma + ' ' + word)
                            break
                        elif word_match == head and word_lemma in mchange_verbs and (
                                word_lemma + ' ' + word) in change_redup:
                            Change_PR_count += 1
                            Change_PR_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                            break
                        elif word_match == head and word_lemma in mchange_verbs and word in ["to"]:
                            if (word_lemma + ' ' + word + ' ' + spacy_words[i + 1]) in change_redup2:
                                Change_PR_count += 1
                                Change_PR_examples.append(head + ' ' + word + spacy_words[i + 1] + ' ("' + the_sentence + '")')
                                break
                        elif word_match == head and word_lemma in mchange_verbs and (word_lemma + ' ' + word) not in exceptions:
                            Change_SF_Count += 1
                            Change_SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                            Change_SF_lemma_examples.append(word_lemma + ' ' + word)
                            break
                        elif word_match == head and word_lemma not in stative_verbs and (
                                word_lemma + ' ' + word) not in exceptions:
                            Unsure_SF_count += 1
                            Unsure_SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                            Unsure_SF_lemma_examples.append(word_lemma + ' ' + word)
                            break

        if pos == "ADV" and word in satellites: #handles particles marked as adverbs as satellites
            if head in satellites and (head + ' ' + word) not in doesnt_count_double_sat:
                Motion_SF_count += 1
                SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
            elif head in list_o_verbs:
                for y in range(0, len(list_o_verbs)):
                    word_match = list_o_verbs[y]
                    word_lemma = list_o_vb_lemmas[y]
                    if word_match == head and (word_lemma + ' ' + word) in path_reduplication:
                        Motion_PR_count += 1
                        PR_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                        break
                    elif word_match == head and (word_lemma + ' ' + word) in counts_as_motion:
                        Motion_SF_count += 1
                        SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                        SF_lemma_examples.append(word_lemma + ' ' + word)
                        break
                    elif word_match == head and word_lemma in mm_verbs and (word_lemma + ' ' + word) not in exceptions:
                        Motion_SF_count += 1
                        SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                        SF_lemma_examples.append(word_lemma + ' ' + word)
                        break
                    elif word_match == head and word_lemma in mchange_verbs and (word_lemma + ' ' + word) in change_redup:
                        Change_PR_count += 1
                        Change_PR_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                        break
                    elif word_match == head and word_lemma in mchange_verbs and (
                            word_lemma + ' ' + word) not in exceptions:
                        Change_SF_Count += 1
                        Change_SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                        Change_SF_lemma_examples.append(word_lemma + ' ' + word)
                        break
                    elif word_match == head and word_lemma not in stative_verbs and (word_lemma + ' ' + word) not in exceptions:
                        Unsure_SF_count += 1
                        Unsure_SF_examples.append(head + ' ' + word + ' ("' + the_sentence + '")')
                        Unsure_SF_lemma_examples.append(word_lemma + ' ' + word)
                        break

        if pos == "VERB":
            if the_lemma in path_verbs and (the_lemma + ' ' + word) not in path_reduplication:
                Motion_VF_count += 1
                VF_examples.append(word + ' ("' + the_sentence + '")')
            elif the_lemma in vchange_verbs and (the_lemma + ' ' + word) not in change_redup and (the_lemma + ' ' + word + ' ' + spacy_words[i+1]) not in change_redup2:
                Change_VF_Count += 1
                Change_VF_examples.append(word + ' ("' + the_sentence + '")')



    final_motion_SF_string = "\n".join(SF_examples)
    final_motion_PR_string = '\n'.join(PR_examples)
    final_motion_VF_string = '\n'.join(VF_examples)
    final_change_SF_string = '\n'.join(Change_SF_examples)
    final_change_VF_string = '\n'.join(Change_VF_examples)
    final_change_PR_string = '\n'.join(Change_PR_examples)
    final_unsure_SF_string = '\n'.join(Unsure_SF_examples)
    return [filename, Motion_SF_count, final_motion_SF_string, Motion_VF_count, final_motion_VF_string, Motion_PR_count,
            final_motion_PR_string, Change_SF_Count, final_change_SF_string, Change_VF_Count, final_change_VF_string,
            Change_PR_count, final_change_PR_string, Unsure_SF_count, final_unsure_SF_string]

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

def process(file_path: str, filename, langauge):
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
        if langauge == "English":
            nlp = spacy.load("en_core_web_lg")
            analysis = nlp(input_text)
            results = get_events(filename, analysis)
            return results

        if langauge == "Japanese":
            nlp = spacy.load("ja_core_news_sm")
            analysis = nlp(input_text)
            results = get_events_j(filename, analysis)
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
    """
    Scores go like this in this order. Number is there for ease of reference.
    (0)filename, (1)Motion_SF_count, (2)final_motion_SF_string, (3)Motion_VF_count, (4)final_motion_VF_string,
    (5)Motion_PR_count, (6)final_motion_PR_string, (7)Change_SF_Count, (8)final_change_SF_string, (9)Change_VF_Count,
    (10)final_change_VF_string, (11)Change_PR_count, (12)final_change_PR_string, (13)Unsure_SF_count,
    (14)final_unsure_SF_string
    :param scores:
    :return:
    """
    string_scores_list = []

    for sc in scores:
        string_score = ""
        string_score += "Filename: " + sc[0] + "\n" + "\n"
        string_score += "Motion Satellite-Framing Count: " + f"{sc[1]}" + "\n" + "\n"
        string_score += "Motion Satellite-Framing Examples: " + "\n" + sc[2] + "\n" + "\n"
        string_score += "Motion Verb-Framing Count: " + f"{sc[3]}" + "\n" + "\n"
        string_score += "Motion Verb-Framing Examples: " + "\n" + sc[4] + "\n" + "\n"
        string_score += "Motion Path Reduplication Count: " + f"{sc[5]}" + "\n" + "\n"
        string_score += "Motion Path Reduplication Examples: " + "\n" + sc[6] + "\n" + "\n"
        string_score += "Change of State Satellite-Framing Count: " + f"{sc[7]}" + "\n" + "\n"
        string_score += "Change of State Satellite-Framing Examples: " + "\n" + sc[8] + "\n" + "\n"
        string_score += "Change of State Verb-Framing Count: " + f"{sc[9]}" + "\n" + "\n"
        string_score += "Change of State Verb-Framing Examples: " + "\n" + sc[10] + "\n" + "\n"
        string_score += "Change of State Path Reduplication Count: " + f"{sc[11]}" + "\n" + "\n"
        string_score += "Change of State Path Reduplication Examples: " + "\n" + sc[12] + "\n" + "\n"
        string_score += "Unsure Satellite-Framing Count: " + f"{sc[13]}" + "\n" + "\n"
        string_score += "Unsure Satellite-Framing Examples: " + "\n" + sc[14] + "\n" + "\n"
        string_score += "\n" + "\n" + "\n"
        string_score += "***************************************"
        string_score += "\n" + "\n"
        string_scores_list.append(string_score)
    return string_scores_list

def main(input_path):
    input_filepath = os.path.join(os.getcwd(), input_path)
    settei_gengo = "English"
    scores = []
    for fdx, filename in enumerate(os.listdir(input_filepath)):
        if filename.endswith('.txt'):
            result = process(os.path.join(input_filepath, filename), filename, settei_gengo)
            scores.append(result)

    string_scores = list_stringify_scores(scores)
    write_data_to_file(string_scores, os.path.join(os.getcwd(), f'./output/EC_Finder_{len(scores)}.txt'))


if __name__ == '__main__':
    main(sys.argv[1])