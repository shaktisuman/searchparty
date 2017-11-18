"""Module represents Shallow NLP pipeline."""
from nltk.corpus import reuters
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import index
import nltk


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
            doc = {'id': i, 'tokens': sentence}
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
        return [self.lemmatizer.lemmatize(t, pos=p) for x, y in zip(sentence, POS)]

    def POS(self, sentence):
        """POS to be added"""
        return



# Driver Code
url = "http://localhost:8983/solr/searchparty"
deepernlp = DeeperPipeline(url, True)
# shallownlp.index_sentences()
shallownlp.search("Malaysia and Japan")
