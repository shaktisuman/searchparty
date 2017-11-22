# Search Party

This project is implemented as part of CS 6320 - Natural Language Processing at University of Texas Dallas by **Harsha Kokel** and **Shakti Suman**.

It is an implemention of a semantic search application that will produce improved results using NLP features and techniques. Project implements a keyword-based strategy and an improved strategy using NLP feature and techniques.

The implementation is divided in 4 parts which were provided as 4 Tasks for the project. The 'Instruction' section in each part is a copy of the Instruction provided where as 'Implementation' section provides the details about our project.

#### 1. Corpus:

###### Instruction  
Create a corpus of News articles. Your corpus should contain at least:  
o 1,000 articles  
o 100,000 words  

Note: you are free to download freely and publicly available News articles corpora from
public websites such as: http://www.nltk.org/nltk_data/

###### Implementation  

We would be working with **The Reuters-21578 benchmark corpus, ApteMod version** corpus of NLTK.

Details of the corpus are mentioned below.

*id*: reuters  
*size*: 6378691  
*license*: The copyright for the text of newswire articles and Reuters annotations in the Reuters-21578 collection resides with Reuters Ltd. Reuters Ltd. and Carnegie Group, Inc. have agreed to allow the free distribution of this data **for research purposes only**. If you publish results based on this data set, please acknowledge its use, refer to the data set by the name 'Reuters-21578, Distribution 1.0', and inform your readers of the current location of the data set.  
*url*: http://www.nltk.org/nltk_data/


#### 2. Shallow NLP Pipeline:

###### Instruction  
Implement a shallow NLP pipeline to perform the following:  
- Keyword search index creation  
  - [x]  Segment the News articles into sentences  
  - [x]  Tokenize the sentences into words  
  - [x]  Index the word vector per sentence into search index such as Lucene or SOLR  
- Natural language query parsing and search  
  - [x]  Segment an user’s input natural language query into sentences  
  - [x]  Tokenize the sentences into words  
  - [x]  Run a search/match with the search query word vector against the sentence word vector (present in the Lucene/SOLR search index) created from the corpus  
- Evaluate the results of at least 10 search queries for the top-10 returned sentence matches

###### Implementation

We used solrpy, a python client for the Solr search service to index the word vector for each sentences.

**index.py** file includes the implementation of wrapper class which uses solrpy to index sentences in solr.

**shallowpipeline.py** file includes the implementation of shallow nlp pipeline as per task 2.

### 3. Deeper NLP pipeline:  

###### Instruction  
Implement a deeper NLP pipeline to perform the following: o Semantic search index creation
- Segment the News articles into sentences
  - [x] Tokenize the sentences into words
  - [x] Lemmatize the words to extract lemmas as features
  - [x] Stem the words to extract stemmed words as features
  - [ ] Part-of-speech (POS) tag the words to extract POS tag features
  - [ ] Syntactically parse the sentence and extract phrases, head words, OR dependency parse relations as features
  - [ ] Using WordNet, extract hypernymns, hyponyms, meronyms, AND holonyms as features
  - [ ] Index the various NLP features as separate search fields in a search index such as Lucene or SOLR
- Natural language query parsing and search
  - [ ] Run the above described deeper NLP on an user’s input natural language and extract search query features
  - [ ] Run a search/match against the separate or combination of search index fields created from the corpus
- Evaluate the results of at least 10 search queries for the top-10 returned sentence matches


###### Implementation  

- [ ] To be added..

#### 4. Improve result:

###### Instruction  
Improve the shallow NLP pipeline results using a combination of deeper NLP pipeline features

###### Implementation  

- [ ] To be added..

---

#### Prerequisite

To make this project work, we will need following setups.

1.  Install Python 2.7
2.  Download reuters corpus.

    ```python  
    >>> import nltk
    >>> nltk.download('reuters')
    ```

3. Install solr
4. Use the managed-schema in the resources folder to create a core in Solr.
5. Install solrpy

    ```bash
    $ sudo pip install solrpy
    ```
6. Download stanford parser
7. Download stanford NER tagger


---
## References

- [ ] To be added..

1. https://blog.manash.me/configuring-stanford-parser-and-stanford-ner-tagger-with-nltk-in-python-on-windows-f685483c374a

#### Note:
You are free to implement or use a third-party tool such as:
1. NLTK: http://www.nltk.org/
2. Stanford NLP: http://nlp.stanford.edu/software/corenlp.shtml
3. Apache OpenNLP: http://opennlp.apache.org/
