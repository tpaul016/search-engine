from searchapp.knn import knn, build_content 
from searchapp.index_and_dict import indexAccess
import json


#build_content.build_content()
inverIndex = indexAccess.getInvertedIndex('searchapp/index_and_dict/reutersIndex.json')
with open("searchapp/knn/content_map.json", 'r') as f:
    c_map= json.load(f)

knn.knn(inverIndex, c_map)
