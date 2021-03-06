from elasticsearch import Elasticsearch
from datetime import datetime
import sys

class SearchEngine():
	def __init__(self, index_name):
		self.es = Elasticsearch()
		self.index_name = index_name

	def add_document(self, id, title, tags, parentid, doctype, body):
		self.es.index(index=self.index_name, id = id, doc_type=doctype, body={"title": title, "tags": tags, "parent_id": parentid, "content": body, "timestamp": datetime.now()})
		print('added document ', title)

	def search(self, query, tags = None):
		#res = es.search(index="asgn3", body={"query": {"match_all": {}}})
		if tags is None:
			res = self.es.search(index=self.index_name, body={"query": {"match": {"content": query}}})
		else:
			res = self.es.search(index=self.index_name, body={"query": {"match": {"content": query, "tags": tags}}})
		return res;

	def deleteIndex(self):
		self.es.indices.delete(index=self.index_name, ignore=[400, 404])

	def countDocs(self):
		res = self.es.count(index=self.index_name)
		return res

def main():

	query = sys.argv[1]
	index_name = 'df'
	fts = SearchEngine(index_name);
	results = fts.search(query)
	results = results['hits']['hits']
	for result in results:
		print result['_type'];
		print result['_source']['title'];
		print result['_source']['tags'];

	#fts.deleteIndex()
	#print fts.countDocs()

if __name__ == "__main__":
	main()
