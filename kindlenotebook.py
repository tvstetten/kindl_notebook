'''
Copy the content of https://read.amazon.com/notebook
'''
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import pyperclip
import google.generativeai as genai

load_dotenv()

AI_MODEL = os.environ.get("AI_MODEL") or ""
API_KEY= os.environ.get("GEMENI_API_KEY")
OBSIDIAN_PATH = os.environ.get("OBSIDIAN_PATH")


EXAMPLE = """Your Kindle Notes For:
Match Game (Expeditionary Force Book 14)
Craig Alanson
Last accessed on Wednesday February 19, 2025
21 Highlight(s) | 0 Note(s)
Yellow highlight | Location: 8,925
chided


Yellow highlight | Location: 8,944
reprieve


Yellow highlight | Location: 9,029
devious


Yellow highlight | Location: 9,034
dreaded


Yellow highlight | Location: 9,046
sauteed


Yellow highlight | Location: 9,062
exclaimed,


Yellow highlight | Location: 9,070
revelation,


Yellow highlight | Location: 9,077
nefarious


Yellow highlight | Location: 9,149
deviousness


Yellow highlight | Location: 9,192
startled


Yellow highlight | Location: 9,295
bogus


Yellow highlight | Location: 9,332
smug


Yellow highlight | Location: 9,334
ointment


Yellow highlight | Location: 9,357
lucid


Yellow highlight | Location: 9,368
retorted.


Yellow highlight | Location: 9,400
salvage


Yellow highlight | Location: 9,412
It was my call. I


Yellow highlight | Location: 9,446
veered


Yellow highlight | Location: 9,590
heinous


Yellow highlight | Location: 9,618
heinous


Yellow highlight | Location: 9,866
ruse,

Yellow highlight | Location: 9,866
give up


"""

test_1 = '''
    i have a list of english words: ["chided", "reprieve", "dreaded"] please list this words and get up to 3 german translations for every word. In Addition for every word give me 3 english sentences using that word as well as the german translation for the sentence
'''

prompt_template = '''
I have a list of english words or phrases:

[$$LIST$$]

As a result build a json-structure with the following format:
[
    {
        "original": {uncorrected original word from the list}
        "english": {word},
        "german": [
            {german_translations},...
        ]
        "tenses": [
            {infinitive},
            {past},
            {past_participle}
        ]
        "word_type": {word_type}
        "sentences": [
            {
                "english": {sentence_english},
                "german": {sentence
            }
        ]
    },
    {...}
]

For every word in that list:
- if it is a verb build the infinitive and continue with this infinitive as the word
- if the word is a noun capitalize the first character
- if it is plural build the singular (without a comment)

- Add the original list-entry
- Add the entry "word"
- If the word is a "verb" or a "phrasal verb" build a list with the infinitive, the past and the past participle of the verb
- If the word is not a phrase and not a noun convert the english word to lowercase
- If word is a single word add 5 german translations of the word sorted by relevance else if word is a phrasal verb add 5 german translations of the word sorted by relevance else if the word is a phrase (not a phrasal verb) add the translation the phrase as a list with one entry "german"
- Add a list of 3 english sentences using the word as well as the german translation for the sentence. Mark the word and the translated german word in the sentences as bold

Please provide the pure json without comments.'''

def extract_highlights():
    # Inhalt der Zwischenablage abrufen
    clipboard_content = pyperclip.paste()
    # clipboard_content = EXAMPLE

    # Inhalt in Zeilen aufteilen
    lines = clipboard_content.split('\n')

    # Text extrahieren, der der Zeile mit 'highlight |' folgt
    highlights = []
    for i in range(len(lines)):
        if 'highlight |' in lines[i]:
            text = lines[i + 1].strip().replace('"', '')
            highlights.append(text)

    return highlights

def add_list_yaml(list: list[str], key: str, items: None|list[str], force: bool=False):
    '''Add a list to a yaml list'''
    if items or force:
        list.append(f'{key}:')
        if items:
            list.extend([f'  - {item}' for item in items])


def create_file(original: str, english: str, germans: list, raw_sentences: list[dict[str, str]], tenses: list, word_type: str):
    file_name = f"{OBSIDIAN_PATH}{english} - {germans[0]}.md"
    # Current date in the given format
    current_datetime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    # File-Content; starting with the YAML front matter
    content = [
        '---',
        f'created: {current_datetime}',
        'creator: Thomas von Stetten'
    ]
    add_list_yaml(content, 'tags', ['dictionary/eng_ger'])
    content.extend([
        f'word_type: {word_type}',
        f'english: {english}',
    ])
    add_list_yaml(content, 'german', germans)
    add_list_yaml(content, 'tenses', tenses)
    content.extend([
        '---',
        '## Example Sentences',
        "|English|German|",
        "|---|---|"
    ])
    content.extend([f"|{sentence['english']}|{sentence['german']}|" for sentence in raw_sentences])

    # Inhalte in Datei schreiben
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write("\n".join(content))

def main_read_clipboard():
    # Highlights extrahieren und ausgeben
    highlights = extract_highlights()

    list = f'''["{'","'.join(highlights) }"]'''
    prompt = prompt_template.replace("[$$LIST$$]", list)

    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(model_name=AI_MODEL)

    print(prompt)
    print()
    print(f"asking AI (Model: {AI_MODEL})")
    response = model.generate_content(prompt)
    # >The result looks like:
    # #'```json\n{\n  "words": [\n    {\n      "word": "chide",\n      "german_translations": ["schelten", "tadeln", "verweisen", "zurechtweisen", "rügen"],\n      "word_type": "(verb)",\n      "sentences": [\n        {\n          "english": "He **chided** his son for his bad behavior.",\n          "german": "Er **schalt** seinen Sohn wegen seines schlechten Verhaltens."\n        },\n        {\n          "english": "Don\'t **chide** me for making a mistake.",\n          "german": "**Tadel** mich nicht, weil ich einen Fehler gemacht habe."\n        },\n        {\n          "english": "The teacher **chided** the class for their noise.",\n          "german": "Die Lehrerin **verwies** die Klasse wegen des Lärms."\n        }\n      ]\n    },\n    {\n      "word": "Reprieve",\n      "german_translations": ["Aufschub", "Vertagung", "Gnade", "Begnadigung", "Aussatz"],\n      "word_type": "(noun)",\n      "sentences": [\n        {\n          "english": "The prisoner received a **reprieve**.",\n          "german": "Der Gefangene erhielt einen **Aufschub**."\n        },\n        {\n          "english": "The judge granted a **Reprieve** to the condemned man.",\n          "german": "Der Richter gewährte dem zum Tode Verurteilten eine **Begnadigung**."\n        },\n        {\n          "english": "The news brought a temporary **Reprieve** from their worries.",\n          "german": "Die Nachricht brachte einen vorübergehenden **Aufschub** ihrer Sorgen."\n        }\n      ]\n    },\n    {\n      "word": "dread",\n      "german_translations": ["fürchten", "furcht", "angst", "schaudern", "erschrecken"],\n      "word_type": "(verb)",\n      "sentences": [\n        {\n          "english": "I **dread** the upcoming exam.",\n          "german": "Ich **fürchte** die bevorstehende Prüfung."\n        },\n        {\n          "english": "Many people **dread** public speaking.",\n          "german": "Viele Menschen **fürchten** sich vor öffentlichen Reden."\n        },\n        {\n          "english": "She **dreaded** telling him the bad news.",\n          "german": "Sie **erschrak** davor, ihm die schlechte Nachricht zu erzählen."\n        }\n      ]\n    }\n  ]\n}\n```\n'
    json_response = json.loads(response.text[8:-5])

    for response in json_response:
        original = response["original"]
        english = response["english"]
        print(f"handling {english} ({original})")
        germans = response["german"]
        tenses= response.get("tenses", None)
        word_type = response["word_type"]
        raw_sentences = response["sentences"]

        # Datei für jedes Highlight erstellen
        create_file(original, english, germans, raw_sentences, tenses, word_type)

    print("done")

if __name__ == "__main__":
    main_read_clipboard()
