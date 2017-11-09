"""Module represents wrapper for solr."""
import solr


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

        self.conn = solr.SolrConnection(url)

    def add(self, doc):
        """Index the document in solr."""
        print self.conn.add(id=doc["id"], tokens=doc["tokens"])
        self.conn.commit()

    fields = ["id", "tokens"]


# Driver Code:
# url = "http://localhost:8983/solr/searchparty"
# s = SolrSearch(url)
# doc = {'id': '3', 'tokens': ['harsha', 'is', 'good', '.']}
# s.add(doc)
