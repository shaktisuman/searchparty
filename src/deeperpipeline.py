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
from nltk.tag.perceptron import PerceptronTagger
from nltk.corpus import wordnet


os.environ['CLASSPATH'] = '../resources/stanford-ner-2017-06-09:../resources/stanford-parser-full-2017-06-09'
os.environ['JAVAHOME'] = '/usr/bin/java'
os.environ['STANFORD_MODELS'] = '../resources/stanford-ner-2017-06-09/classifiers:../resources/stanford-parser-full-2017-06-09'


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
        self.dep_parser = StanfordDependencyParser(model_path='edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')
        self.parser = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
        self.nertagger = StanfordNERTagger('english.muc.7class.distsim.crf.ser.gz')

    def index_sentences(self):
        """Index the sentences of the corpus."""
        i = 0
        for sentence in self.getSentences():
            stems = self.stem(sentence)
            dependency_parse, headword = self.dep_parse_and_headword(sentence)
            named_entities = self.ner_tag(sentence)
            POS = self.POS(sentence)
            lemma = self.lemma(sentence, POS)
            hypernym = self.hypernym(sentence)
            hyponym = self.hyponym(sentence)
            substance_meronym = self.substance_meronym(sentence)
            member_meronym = self.member_meronym(sentence)
            part_meronym = self.part_meronym(sentence)
            substance_holonym = self.substance_holonym(sentence)
            member_holonym = self.member_holonym(sentence)
            part_holonym = self.part_holonym(sentence)
            doc = {'id': i, 'tokens': sentence, 'stem': stems,
                   'parse': dependency_parse, 'headword': headword,
                   'named_entities': named_entities, 'POS': POS, 'lemma': lemma, 'hypernym': hypernym, 'hyponym': hyponym, 'substance_meronym': substance_meronym, 'member_meronym': member_meronym, 'part_meronym': part_meronym, 'substance_holonym': substance_holonym, 'member_holonym': member_holonym, 'part_holonym': part_holonym}
            self.solr.add(doc)
            # print doc
            i = i+1

    def getSentences(self):
        """Return 100 sentences if testrun, all sentences otherwise."""
        if self.testrun:
            return reuters.sents()[0:5]
        else:
            return reuters.sents()

    def search(self, sentence):
        """Return top 10 relevant search result for given string."""
        docs = self.solr.query(word_tokenize(sentence))
        for doc in docs:
            print " ".join(doc["tokens"])

    def stem(self, sentence):
        """Return the list of stem for given sentence."""
        return [self.stemmer.stem(x) for x in sentence]

    def lemma(self, POS):
        """Return the list of lemmatized word for given sentence."""
        lemma = []
        for p in POS:
            if self.penn_to_wn(p[1]) is None:
                lemma.append(self.lemmatizer.lemmatize(p[0]))
            else:
                lemma.append(self.lemmatizer.lemmatize(p[0], pos=self.penn_to_wn(p[1])))
        return lemma

    def POS(self, sentence):
        """Return Perceptron Pre-trained POS tags for words in a sentence."""
        pretrain = PerceptronTagger()
        return pretrain.tag(sentence)

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
    
    def hypernym(self, sentence):
        """Return Wordnet based Hypernyms of words in a sentence."""
        hypernym_list = []
        for words in sentence.split():
            hypernyms = (wordnet.synsets(words))[0].hypernyms()
            hypernym_list.append(hypernyms[0].name().split(".")[0])
        return hypernym_list
    
    def hyponym(self, sentence):
        """Return Wordnet based Hyponyms of words in a sentence."""
        hyponym_list = []
        for words in sentence.split():
            hyponym_all = (wordnet.synsets(words))[0].hyponyms()
            #Considering first hyponym in wordnet
            hyponym_list.append(hyponym_all[0].name().split(".")[0])
        return hyponym_list
    
    def substance_meronym(self, sentence):
        """Return Wordnet based Meronyms of words in a sentence."""
        substance_meronyms_list = []
        for words in sentence.split():
            meronyms = (wordnet.synsets(words))[0].substance_meronyms()
            if len(meronyms) is not 0:
                substance_meronyms_list.append(meronyms[0].name().split(".")[0])
            else:
                substance_meronyms_list.append("")
        return substance_meronyms_list
    
    def member_meronym(self, sentence):
        """Return Wordnet based Meronyms of words in a sentence."""
        member_meronyms_list = []
        for words in sentence.split():
            meronyms = (wordnet.synsets(words))[0].member_meronyms()
            if len(meronyms) is not 0:
                member_meronyms_list.append(meronyms[0].name().split(".")[0])
            else:
                member_meronyms_list.append("")
        return member_meronyms_list
    
    def part_meronym(self, sentence):
        """Return Wordnet based Meronyms of words in a sentence."""
        part_meronyms_list = []
        for words in sentence.split():
            meronyms = (wordnet.synsets(words))[0].part_meronyms()
            if len(meronyms) is not 0:
                part_meronyms_list.append(meronyms[0].name().split(".")[0])
            else:
                part_meronyms_list.append("")
        return part_meronyms_list
    
    def substance_holonym(self, sentence):
        """Return Wordnet based Holonyms of words in a sentence."""
        substance_holonym_list = []
        for words in sentence.split():
            holonyms = (wordnet.synsets(words))[0].substance_holonyms()
            if len(holonyms) is not 0:
                substance_holonym_list.append(holonyms[0].name().split(".")[0])
            else:
                substance_holonym_list.append("")
        return substance_holonym_list
    
    def member_holonym(self, sentence):
        """Return Wordnet based Holonyms of words in a sentence."""
        member_holonym_list = []
        for words in sentence.split():
            holonyms = (wordnet.synsets(words))[0].member_holonyms()
            if len(holonyms) is not 0:
                member_holonym_list.append(holonyms[0].name().split(".")[0])
            else:
                member_holonym_list.append("")
        return member_holonym_list
    
    def part_holonym(self, sentence):
        """Return Wordnet based Holonyms of words in a sentence."""
        part_substance_holonym_list = []
        for words in sentence.split():
            holonyms = (wordnet.synsets(words))[0].part_holonyms()
            if len(holonyms) is not 0:
                part_substance_holonym_list.append(holonyms[0].name().split(".")[0])
            else:
                part_substance_holonym_list.append("")
        return part_substance_holonym_list

    def penn_to_wn(self, tag):
        """Map Penn tag to Wordnet tag."""
        if tag in ['JJ', 'JJR', 'JJS']:
            return wordnet.ADJ
        elif tag in ['NN', 'NNS', 'NNP', 'NNPS']:
            return wordnet.NOUN
        elif tag in ['RB', 'RBR', 'RBS']:
            return wordnet.ADV
        elif tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
            return wordnet.VERB
        return


# Driver Code
# url = "http://localhost:8983/solr/searchparty"
# deepernlp = DeeperPipeline(url, True)
# deepernlp.index_sentences()
# deepernlp.search("Malaysia and Japan")
