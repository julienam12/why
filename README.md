## Experiments

- [whybot](http://stanford.edu/~erindb/explanations/whybot.html)

    explain daily activities recursively (5 levels deep)

    analysis uses [Hiroyoshi Komatsu and Johannes Castner corenlp wrapper](https://bitbucket.org/torotoki/corenlp-python/src)

- advicebot
- goalbot
- explanations

## How to use submiterator mturk tools

    scripts/_shared/submiterator.py [PATH_TO_CONFIG_FILE] [PATH_TO_OUTPUT_DIRECTORY]
    scripts/_shared/posthit.sh [PATH_TO_MTURK_FILES_WITH_LABEL]
    scripts/_shared/getresults.sh [PATH_TO_MTURK_FILES_WITH_LABEL]
    scripts/_shared/parsedata.py [PATH_TO_RESULTS_FILE] [PATH_TO_OUTPUT_FILE]

For example:

    scripts/_shared/submiterator.py experiments/test/test.config data/test/mturk/
    scripts/_shared/posthit.sh data/test/mturk/test
    scripts/_shared/getresults.sh data/test/mturk/test
    scripts/_shared/parsedata.py data/test/mturk/test.results data/test/mturk/test.csv

## Background

What is "why"?

How do we answer "why" questions?

Why do we answer what we do when people ask us "why"?

### WhyBot: The Automated 3-year-old

The whybot asks participants to explain one of several seeds, then asks them to explain their explanation, etc.. We elicit many Q&A pairs, e.g. "Amy ate a sandwich because Amy was hungry." "Amy was hungry because Amy hadn't eaten in several hours."

current seeds:

* John went to the store
* Jane went to the post office
* Alex did the dishes
* Tom cooked dinner
* Maya drove to work
* Amy ate a sandwich
* Jack read a book about gardening
* Meg bought a new computer
* Sam repaired his bicycle

TODO: make an elicitation.js containing common code that all bots use.

TODO: make a whybot of the same form as above, but ask people to tell us something they know a lot about and explain that.

## Cavemanese

We translate the natural-language whybot results to a simplified, structured form.

    python scripts/whybot/reformat-whybot.py data/whybot/mturk/whybot.results data/whybot/whybot.tsv
    python scripts/whybot/pronoun-resolution.py data/whybot/whybot.tsv data/whybot/pronoun-resolved.tsv
    python scripts/whybot/dependency-parse.py data/whybot/pronoun-resolved.tsv data/whybot/dependency-parsed.tsv