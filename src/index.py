"""Module represents wrapper for solr."""
import solr
from urllib2 import urlopen


class SolrSearch:
    """A wrapper class for searchparty Solr index.

    Attributes:
        url   The Solr URL for the collection

    """

    def __init__(self, url):
        """Initialize the wrapper with the search url.

        Args:
            url (string) The Solr URL for the searchparty collection
        """
        self.url = url
        self.conn = solr.SolrConnection(url)

    def add(self, doc):
        """Index the document in solr."""
        self.conn.add(id=doc["id"], tokens=doc["tokens"], stem=doc["stem"],
                      parse=doc["parse"], headword=doc["headword"], named_entities=doc['named_entities'],
                      POS=doc["POS"], lemma=doc["lemma"], hypernym=doc["hypernym"], hyponym=doc["hyponym"],
                      substance_meronym=doc["substance_meronym"], member_meronym=doc["member_meronym"],
                      part_meronym=doc["part_meronym"], substance_holonym=doc["substance_holonym"] ,
                      member_holonym=doc["member_holonym"], part_holonym=doc["part_holonym"])
        self.conn.commit()

    def query(self, tokens):
        """Query input tokens."""
        query_url = self.url+"/select?q="
        query_url = query_url + "+".join(tokens)  # Query OR between tokens
        # query_url = query_url + "%20AND%20".join(tokens) # This is for AND
        print query_url
        connection = urlopen(query_url)
        response = eval(connection.read())
        print "query formed: ", query_url
        print response['response']['numFound'], "documents found."
        return response['response']['docs']


# fields = ["id", "tokens"]


# Driver Code:
# url = "http://localhost:8983/solr/searchparty"
# s = SolrSearch(url)
# doc = {'id': '3', 'tokens': ['harsha', 'is', 'good', '.']}
# s.add(doc)
# s.query(["the","and"])
