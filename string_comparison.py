from copy import copy
from basic_info import str_comp_weights

#从str1的第一个字符开始寻找在str2中的位置，然后看下一个字符是否相同直至不一致为止，最后删除已比较的字符。
#剩余字符同理。根据相同的串长计算字符串相似度。

def strComp(str1,str2):
	if len(str1)==0 and len(str2)==0:
		return 1.0  #两者均为空行
	else:
		if len(str1)==0 or len(str2)==0:
			return 0.0  #两者其一为空行
	str1cpy=str1
	str2cpy=str2
	i=0  #比较的游标
	simCount=0  #相同字符串长度计数
	while len(str1cpy)!=0 and len(str2cpy)!=0:
		if len(str1cpy)>len(str2cpy):
			strA=str1cpy
			strB=str2cpy
			mode=1  #标记当前strA和strB的实际指向
		else:
			strA=str2cpy
			strB=str1cpy
			mode=2  #标记当前strA和strB的实际指向
		#if strA[0] in [' ', '\t']:
		#	strA=strA[1:]  #去掉开头的空字符
		#	if mode==1:
		#		str1cpy=strA
		start=strB.find(strA[0])
		if start==-1:
			strA=strA[1:]
			if mode==2:
				str2cpy=strA
			else:
				str1cpy=strA
		else:
			i=start
			while i<len(strB) and i-start<len(strA) and strA[i-start]==strB[i]:
				if i-start>0:  #当相似字符串长度>1时才算入相似计数
					simCount+=1
				i+=1
			if i-start>1:
				simCount+=1  #校正相似计数，补齐忽略掉的第一个相似字符(条件+1是因为while处不匹配时i已经+1）
			if mode==1:
				str1cpy=strA[i-start:]
				str2cpy=strB[:start]+strB[i:]
			else:
				str2cpy=strA[i-start:]
				str1cpy=strB[:start]+strB[i:]
			i=0
	#return simCount/max(len(str1),len(str2))
	return simCount/len(str1)  #这样更具双向对比意义

def string_comparison(file_content_1,file_content_2,mode):  #mode 1为函数内部顺序往下对比，2为取函数内容行最大相似值(更激进）
	splited_content_1=split_block(file_content_1)
	splited_content_2=split_block(file_content_2)
	import_comp_result=[]
	func_comp_result=[]
	other_comp_result=[]
	temp_result=[]  #存储逐行比对结果等待取最大值
	offset=0  #当某部分不存在时将其权重分给其他部分的补偿倍数
	parts=['import','other']
	import_line_length_sum=0
	other_line_length_sum=0
	single_function_line_length_sum=0
	for part in parts:
		for line_1 in splited_content_1[part]:
			for line_2 in splited_content_2[part]:
				temp_result.append(strComp(line_1,line_2))  #将content1中每一行和content2的该部分所有行对比
			if part=='import':
				if len(temp_result)==0:
					#import_comp_result.append(0)  #当该部分为空时，无结果则不加入
					pass
				else:
					import_line_length_sum+=len(line_1)
					import_comp_result.append(max(temp_result)*len(line_1))  #取该行和content2此部分最大相似值*该行长度加入该部分结果集
			else:
				if len(temp_result)==0:
					pass
					#other_comp_result.append(0)  #同上
				else:
					other_line_length_sum+=len(line_1)
					other_comp_result.append(max(temp_result)*len(line_1))  #同上
			temp_result=[]
	if len(import_comp_result)==0:    #暂时各部分取相似度平均值
		offset+=str_comp_weights['import']
		import_result=0  #如果该部分没有对比结果，记录补偿倍数（其他部分权重扩大）
	else:
		if import_line_length_sum!=0:
			#import_result=sum(import_comp_result)/len(import_comp_result)*str_comp_weights['import']  #算术平均
			import_result=sum(import_comp_result)/import_line_length_sum*str_comp_weights['import']  #加权平均
		else:
			import_result=0  #有比较结果没有行长度，基本不可能
	if len(other_comp_result)==0:
		offset+=str_comp_weights['other']
		other_result=0
	else:
		if other_line_length_sum==0:
			other_result=sum(other_comp_result)/other_line_length_sum*str_comp_weights['other']
		else:
			other_result=0  #有比较结果没有行长度，基本不可能
	if mode==1:
		for func_1 in splited_content_1['functions']:
			temp_result=[]
			single_function_line_length_sum=0
			for func_2 in splited_content_2['functions']:
				func_line_temp_result=[]
				i=0
				while i<len(func_1) and i<len(func_2):
					func_line_temp_result.append(strComp(func_1[i],func_2[i])*len(func_1[i]))
					single_function_line_length_sum+=len(func_1[i])
					i+=1
				if i!=0:
					if single_function_line_length_sum!=0:
						temp_result.append(sum(func_line_temp_result)/single_function_line_length_sum)
					else:
						temp_result.append(0)  #函数完全为空，不太可能
				else:
					#temp_result.append(0)
					pass
			if len(temp_result)!=0:
				func_comp_result.append(max(temp_result))  #函数相似度取最大值
	elif mode==2:
		for func_1 in splited_content_1['functions']:
			temp_result=[]
			single_function_line_length_sum=0
			for func_2 in splited_content_2['functions']:
				#fun_2_content=copy(func_2)
				func_temp_result=[]
				for line_1 in func_1:
					func_line_temp_result=[]
					#for line_2 in fun_2_content:
					for line_2 in func_2:
						func_line_temp_result.append(strComp(line_1,line_2))
					single_function_line_length_sum+=len(line_1)
					func_temp_result.append(max(func_line_temp_result)*len(line_1))
					#fun_2_content.remove(fun_2_content[func_line_temp_result.index(max(func_line_temp_result))])
					#从func_2副本去除参考样本中已比较的行
				if single_function_line_length_sum!=0:
					temp_result.append(sum(func_temp_result)/single_function_line_length_sum)
				else:
					temp_result.append(0)  #函数完全为空，不太可能
			if len(temp_result)!=0:
				func_comp_result.append(max(temp_result))
	#return {'import':sum(import_comp_result)/len(import_comp_result),\
	#	'functions':sum(func_comp_result)/len(func_comp_result),\
	#	'other':sum(other_comp_result)/len(other_comp_result)}  #暂时各部分取相似度平均值
	if len(func_comp_result)==0:
		offset+=str_comp_weights['func']
		func_result=0
	else:
		func_result=sum(func_comp_result)/len(func_comp_result)*str_comp_weights['func']
	
	if offset<1:  #当offset==1时意味所有部分都没有可对比的
		final_result=(import_result+func_result+other_result)/(1-offset)
	else:
		final_result=0
	return {'status':True,'result':final_result}


def split_block(file_content):  #将文件内容按照函数和import、class、注释等分块
	import_content=[]
	function_content=[]
	functions=[]
	other_content=[]
	for line in file_content:
		if 'import ' in line and (line.find('import')==0 or line[line.find('import')-1] in ['/t',' ']):  #关键字留出空格是为了防止匹配到变量名
			import_content.append(line)
			continue
		elif 'class ' in line and (line.find('class')==0 or line[line.find('class')-1] in ['/t',' ']):
			other_content.append(line)
			continue
		elif line.strip()[0]=='#':
			other_content.append(line)
			continue
		elif 'def ' in line and (line.strip().find('def')==0 or line[line.find('def')-1] in ['/t',' ']):
			if len(function_content)>0:
				functions.append(function_content)
				function_content=[]
			function_content.append(line)
		else:
			function_content.append(line)  #其余的算作函数的内容
	if len(function_content)!=0:
		functions.append(function_content)
	result={'import':import_content,'functions':functions,'other':other_content}
	return result
