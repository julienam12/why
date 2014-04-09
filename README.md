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

### Cavemanese

We translate the natural-language whybot results to a simplified, structured form.

### NLP Server Setup

1. get access to a server with at least 3GB of ram and permissions for http requests

1. ssh onto this server

        ssh username@server-address

1. install some dependencies (if necessary)

        sudo apt-get install git python-pexpect python-unidecode

    **NB** `python-unidecode` is not necessary. If (you're on AFS, which doesn't already have unidecode installed, and) you don't have sudo privileges, make the following changes:

            * comment out line 24

                from unidecode import unidecode

            * change line 68 to

                for line in text.split("\n"):

1. download [dasmith's stanford-corenlp-python wrapper](https://github.com/dasmith/stanford-corenlp-python)

        git clone git://github.com/dasmith/stanford-corenlp-python.git

1. download [stanford's core nlp tools](http://nlp.stanford.edu/software/corenlp.shtml) INSIDE the dasmith folder

        cd stanford-corenlp-python
        wget http://nlp.stanford.edu/software/stanford-corenlp-2012-07-09.tgz
        tar xvfz stanford-corenlp-2012-07-09.tgz

1. start the python nlp wrapper server on your server (here's a fun fact for those of you who, like me, don't know much about servers. "server" apparently means two things: 1. a computer you can access via the internet and 2. a program running on such a computer that handles requests)

        python corenlp.py -H 0.0.0.0 -p 12345

1. in any file that calls the nlp server you've just set up, change the host to the address of your server (or use mine if mine is set up ~ currently running on host corn18.stanford.edu and port 12345)

**NB** If you're using my server (or probably any other server on Stanford's network), you will ONLY be able to connect to the server when you're on Stanford's VPN