import xmnlp
xmnlp.set_model('E:/xmnlp-onnx-models-v3/xmnlp-onnx-models')
with open('test_A.tsv','r',encoding='utf8') as f:
	for i,line in enumerate(f):
		a,b = line.strip().split('\t')
		a = xmnlp.pinyin("".join(spliteKeyWord(a)))
		b = xmnlp.pinyin("".join(spliteKeyWord(b)))
		if a==b:
			with open('test_out.txt','a+',encoding='utf8') as out:
				out.write(str(i)+"\n")
