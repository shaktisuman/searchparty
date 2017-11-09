"""Module represents Shallow NLP pipeline."""
from nltk.corpus import reuters
import index
import nltk


class ShallowPipeline:
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

# Driver Code
url = "http://localhost:8983/solr/searchparty"
shallownlp = ShallowPipeline(url, True)
# shallownlp.index_sentences()
shallownlp.search("Malaysia and Japan")
