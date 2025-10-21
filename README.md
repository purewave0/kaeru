:uk: **English** | [:brazil: Português](README.pt-br.md) (TODO)

# kaeru

Japanese verb & adjective conjugation trainer for learners of all levels.

![kaeru screenshot](assets/screenshot.png "Screenshot")

- Fast and focused practising
- Randomly selects a word (verb/adjective) and a target inflection
- Asks the correct conjugation for the given word
- Vocab generator picks the most common words across Japanese media
- Straightforward, customisable vocabulary JSON
- Shows kana reading, word type
- Streak-based score tracker
- GUI (Qt) & CLI available
- Internationalisation: available in English, [Portuguese](README.pt-br.md)(TODO)
- Cross-platform

The name comes from 変える (to change, to transform) and カエル (frog 🐸), both read as
*kaeru* (kah-**ay**-**roo**).


## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/purewave0/kaeru.git
    cd kaeru
    ```

2. Set up the virtual environment:
    ```sh
    python3 -m venv env
    source env/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Build the project:
    ```sh
    pyside6-project build
    ```


## Usage

First, generate the vocabulary file, which contains all the words used by the quizzer:
```sh
python3 gen-vocab.py
```

Now, run kaeru:
```sh
pyside6-project run
```

If you'd like to practise through the terminal instead, run:
```sh
python3 kaeru-cli.py
```


## Options

### `gen-vocab.py`

| Option | Description |
|--------|-------------|
| `-n`, `--limit-per-type` | the maximum number of verbs and adjectives to fetch (default: 100 each) |
| `-o`, `--output` | where to save the final JSON (default: `vocab.json`) |

### `kaeru.py`

> [!NOTE]
> To pass options, run `kaeru.py` directly instead of using `pyside6-project`.

| Option | Description |
|--------|-------------|
| `-i`, `--vocab-file` | path to the vocab file (default: `vocab.json`) |

In the GUI:

- **View > Kana reading**: whether to show kana readings for words with kanji
- **View > Word type**: whether to show the word type ("5-dan verb", "い-adjective", etc.)
- **Preferences > Reveal answer on failure**: whether to show the correct answer after a failed attempt


### `kaeru-cli.py`

| Option | Description |
|--------|-------------|
| `-i`, `--vocab-file` | path to the vocab file (default: `vocab.json`) |
| `-K`, `--hide-kana` | don't display kana readings for words with kanji |
| `-T`, `--hide-word-type` | don't display the word type
| `-r`, `--reveal-answer` | reveal the correct answer after an incorrect attempt


## Testing

First, install the dependencies:
```sh
pip3 install -r requirements-dev.txt
```

Run all tests with:
```sh
python3 -m pytest
```


## Credits

- [Kuuuube's yomitan-dictionaries](https://github.com/Kuuuube/yomitan-dictionaries) for
the JPDB.io word frequency list JSON
- [JMdict Simplified](https://github.com/scriptin/jmdict-simplified/) for
the JMdict in JSON format
