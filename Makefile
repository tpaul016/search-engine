clean:
	rm searchapp/index_and_dict/index.json

vsmtest:
	rm -rf searchapp/cor_pre_proc/corpus/ 
	cp -r searchapp/cor_pre_proc/testCorpuses/vsmTestCorpus/ searchapp/cor_pre_proc/corpus

