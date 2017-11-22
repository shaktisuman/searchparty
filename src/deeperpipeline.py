"""Module represents Shallow NLP pipeline."""
import index
import os
from nltk.tag import StanfordNERTagger
from nltk.corpus import reuters
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.parse.stanford import StanfordDependencyParser
from nltk.parse.stanford import StanfordParser
from nltk.tokenize import word_tokenize

os.environ['CLASSPATH'] = '/Users/hkokel/UTD/SEM-I/CS 6320 - NLP/Homework/Project/searchparty/resources/stanford-ner-2017-06-09:/Users/hkokel/UTD/SEM-I/CS 6320 - NLP/Homework/Project/searchparty/resources/stanford-parser-full-2017-06-09'
os.environ['JAVAHOME'] = '/usr/bin/java'
os.environ['STANFORD_MODELS'] = '/Users/hkokel/UTD/SEM-I/CS 6320 - NLP/Homework/Project/searchparty/resources/stanford-ner-2017-06-09/classifiers:/Users/hkokel/UTD/SEM-I/CS 6320 - NLP/Homework/Project/searchparty/resources/stanford-parser-full-2017-06-09'


class DeeperPipeline:
    """Implementing ShallowPipeline.

    Attributes:
        url     The Solr URL for the collection
        testrun True/False

    """

    def __init__(self, url, testrun):
        """Initialize the ShallowPipeline.

        Args:
            url (String)       The Solr URL for the collection
            testrun (Boolean)  True if it is a test run, False if need
                               to index full corpus
        """
        self.solr = index.SolrSearch(url)
        self.testrun = testrun
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

    def index_sentences(self):
        """Index the sentences of the corpus."""
        i = 0
        for sentence in self.getSentences():
            stems = self.stem(sentence)
            doc = {'id': i, 'tokens': sentence, 'stem': stems}
            self.solr.add(doc)
            i = i+1

    def getSentences(self):
        """Return 100 sentences if testrun, all sentences otherwise."""
        if self.testrun:
            return reuters.sents()[0:100]
        else:
            return reuters.sents()

    def search(self, sentence):
        """Return top 10 relevant search result for given string."""
        docs = self.solr.query(nltk.word_tokenize(sentence))
        for doc in docs:
            print " ".join(doc["tokens"])

    def stem(self, sentence):
        """Return the list of stem for given sentence."""
        return [self.stemmer.stem(x) for x in sentence]

    def lemma(self, sentence, POS):
        """Return the list of lemmatized word for given sentence."""
        # TO-DO Add Lemma after POS implementation
        return [self.lemmatizer.lemmatize(t, pos=p) for t, p in zip(sentence, POS)]

    def POS(self, sentence):
        """POS to be added."""
        return

    def dep_parse_and_headword(self, sentence):
        """Return the dependecy list and headword of the given sentence."""
        parse = next(self.dep_parser.raw_parse(' '.join(sentence)))
        dependency = list(parse.triples())
        headword = parse.tree().label()
        return dependency, headword

    def ner_tag(self, sentence):
        """Return Named Entities from the sentence."""
        named_entities = []
        for x, y in self.nertagger.tag(sentence):
            if y != 'O':
                named_entities.append((x, y))
        return named_entities

# Driver Code
url = "http://localhost:8983/solr/searchparty"
deepernlp = DeeperPipeline(url, True)
deepernlp.index_sentences()
deepernlp.search("Malaysia and Japan")
