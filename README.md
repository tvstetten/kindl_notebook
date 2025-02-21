# Kindle Notebook

This project extracts highlights from Kindle notes and generates markdown files with translations and example sentences using the Google Generative AI model.

## Features

- Extracts highlights from Kindle notes (using the clipboard).
- Translates English words to German.
- Generates example sentences in both English and German.
- Creates markdown files with the extracted information.

## Requirements

- Python 3.12+
- uv
- `python-dotenv`
- `pyperclip`
- `google-generativeai`

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/kindle-notebook.git
    cd kindle-notebook
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    source venv/bin/activate  # On macOS/Linux
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a [.env](http://_vscodecontentref_/1) file in the project root directory and add your environment variables:

    ```properties
    AI_MODEL=gemini-1.5-flash
    GEMENI_API_KEY=your_gemini_api_key
    OBSIDIAN_PATH=./export/
    ```

## Usage

1. Ensure your Kindle highlights are copied to the clipboard.

2. Run the script:

    ```sh
    python getnotes.py
    ```

3. The script will extract the highlights, translate the words, generate example sentences, and create markdown files in the specified [OBSIDIAN_PATH](http://_vscodecontentref_/2).

## Example

Here is an example of the generated markdown file:

```markdown
---
created: 2025-02-21T12:34:56
creator: Thomas von Stetten
tags: [dictionary/eng_ger]
word_type: (verb)
english: give up
german:
  - aufgeben
  - aufhören
  - verzichten
  - kapitulieren
  - resignieren
tenses:
  - give up
  - gave up
  - given up
---
## Example Sentences
|English|German|
|---|---|
|He **gave up** smoking.|Er hat das Rauchen **aufgegeben**.|
|She **gave up** her seat.|Sie hat ihren Platz **aufgegeben**.|
|They **gave up** hope.|Sie haben die Hoffnung **aufgegeben**.|