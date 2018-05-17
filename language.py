import textwrap
import os
import locale


def open_lang_file(lang):
    prompts_ = dict()
    path = os.sep.join(('languages', lang))
    with open(path, 'r', encoding='utf8') as f:
        for line in f.readlines():
            name, description = line.split(':', 1)
            description = textwrap.fill(description, 110)
            prompts_[name] = description + " "
    return prompts_


def get_prompts():
    try:
        language = locale.getdefaultlocale()[0]
        prompts = open_lang_file(language)
        print(prompts['primary_lang_info'] + "\n" + prompts['secondary_lang_info'], end='')
        change_language_query = input()
        if change_language_query in ('l', 'L'):
            language = 'en_US' if language != 'en_US' else 'tr_TR'
            prompts = open_lang_file(language)
            print(prompts['lang_set_to'])
    except FileNotFoundError:
        select_lang_q = input(
            "We don't have support for your language. "
            "Please choose a language: [1] for English, [2] for Turkish >> ")
        while select_lang_q not in ('1', '2'):
            select_lang_q = input("Unknown command. Please press [1] or [2] >> ")
        if select_lang_q == '1':
            language = "en_US"
        else:
            language = "tr_TR"
        prompts = open_lang_file(language)
        print(prompts['lang_set_to'])
    return prompts
