# Kindle Notebook

This project extracts highlights from Kindle Notebooks and generates markdown files with translations and example sentences using the Google Generative AI model. The markdown files can be used in note-taking apps like Obsidian.

I decided to use the clipboard instead of web scraping because I need to select the book I made the notes on.

## Why I made this

I wanted to create a tool that would help me learn new words and phrases from the books I read on my Kindle. I also wanted to practice my Python skills and learn how to use the Google Generative AI model.

## Features

- Extracts highlights from Kindle notes (using the clipboard).
- Translates English words to German.
- Generates example sentences in both English and German.
- Creates markdown files with the extracted information including YAML front matter.

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

2. Initialize Project and Install the required packages:

    ```sh
    uv sync
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

    goto https://read.amazon.com/notebook find the book with your english words select all and copy to clipboard.

    then run the script:
    ```sh
    python kindlnotebook.py
    ```

## Example

Here is an example of the generated markdown file:

```markdown
---
created: 2025-02-21T12:34:56
creator: Thomas von Stetten
tags: [dictionary/eng_ger]
word_type: verb
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
source: The Oxford Dictionary of English
---
## Example Sentences
|English|German|
|---|---|
|He **gave up** smoking.|Er hat das Rauchen **aufgegeben**.|
|She **gave up** her seat.|Sie hat ihren Platz **aufgegeben**.|
|They **gave up** hope.|Sie haben die Hoffnung **aufgegeben**.|