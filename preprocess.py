import xmnlp
xmnlp.set_model('E:/xmnlp-onnx-models-v3/xmnlp-onnx-models')
with open('test_A.tsv','r',encoding='utf8') as f:
	for i,line in enumerate(f):
		a,b = line.strip().split('\t')
		a = xmnlp.pinyin(a)
		b = xmnlp.pinyin(b)
		if a==b:
			with open('test_out.txt','a+',encoding='utf8') as out:
				out.write(str(i)+"\n")
