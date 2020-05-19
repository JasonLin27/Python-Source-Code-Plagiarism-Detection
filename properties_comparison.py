from word_analyse import Word_Analyser
from basic_info import *

def properties_comp(file_content_1,file_content_2,weight):  #将寻找到的特征加权得出相似度
	ana_result_1=Word_Analyser(file_content_1).get_result()
	ana_result_2=Word_Analyser(file_content_2).get_result()
	var_count=0  #相同变量计数
	const_count=0  #相同常量计数
	empty_properties_offset=0  
	result=0
	if ana_result_1['status']==True and ana_result_2['status']==True:
		if len(ana_result_1['vars'])==0 and len(ana_result_2['vars'])==0:
			var_result=0    #当某种特征为空时将其权重等比例分配到剩下的特征中
			empty_properties_offset+=weight['const']
		elif len(ana_result_1['vars'])==0:
			var_result=0
		else:
			for var_1 in ana_result_1['vars']:  #对比变量相同情况
				if var_1 in ana_result_2['vars']:
					var_count+=1
					#ana_result_2['vars'].remove(var_1)  #去除对比中相同的对象
			var_result=var_count/len(ana_result_1['vars'])
		if len(ana_result_1['consts'])==0 and len(ana_result_2['consts'])==0:
			const_result=0  #当某种特征为空时将其权重等比例分配到剩下的特征中
			empty_properties_offset+=weight['const']
		elif len(ana_result_1['consts'])==0:
			const_result=0
		else:
			for const_1 in ana_result_1['consts']:  #对比常量相同情况
				if const_1 in ana_result_2['consts']:
					const_count+=1
					#ana_result_2['consts'].remove(const_1)
			const_result=const_count/len(ana_result_1['consts'])
		properties_1=extract_properties(ana_result_1['trans_content'])
		properties_2=extract_properties(ana_result_2['trans_content'])
		for item in properties_1:
			if properties_1[item]==properties_2[item]:
				if properties_1[item]==0:
					empty_properties_offset+=weight[item]
				else:
					result+=weight[item]
			else:
				pass
		#if properties_1['func']==properties_2['func']:
		#	result+=weight['func']
		#if properties_1['judge_stru']==properties_2['judge_stru']:
		#	result+=weight['judge']
		#if properties_1['loop_stru']==properties_2['loop_stru']:
		#	result+=weight['loop']
		#if properties_1['error_stru']==properties_2['error_stru']:
		#	result+=weight['error']
		#if properties_1['arith_op']==properties_2['arith_op']:
		#	result+=weight['arith_op']
		#if properties_1['value_assign']==properties_2['value_assign']:
		#	result+=weight['value_assign']
		if empty_properties_offset==1:
			final_result=0  #模仿strComp法的补偿计算，待验证
		else:
			final_result=result+var_result*weight['var']\
			+const_result*weight['const']/(1-empty_properties_offset)
		status=True
		#return {'status':status,'result':final_result}
	else:
		status=ana_result_1['status']
		final_result=-1
		#print("对比的文件词法分析失败")
	return {'status':status,'result':final_result}
				
def extract_properties(trans_content):
	func_count=0
	judgement_stru_count=0
	loop_stru_count=0
	error_handle_count=0
	arith_op_count=0
	value_assign_count=0
	for line in trans_content:
		if str(KEY_CODE['def'])+'K' in line:
			func_count+=1
		if str(KEY_CODE['elif'])+'K' in line or str(KEY_CODE['if'])+'K' or str(KEY_CODE['else'])+'K' in line:
			judgement_stru_count+=1
		if str(KEY_CODE['for'])+'K' in line or str(KEY_CODE['while'])+'K' in line:
			loop_stru_count+=1
		if str(KEY_CODE['try'])+'K' in line or str(KEY_CODE['with'])+'K' in line:
			error_handle_count==1
		code_list=line[1].split(' ')
		for code in code_list:  #这么写可以作更详细的运算类型统计，但暂时统一记为运算操作
			if str(SYM_CODE['+'])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['-'])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['*'])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['/'])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['%'])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['<<'])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['>>'])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['&'])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['|'])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['**='])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['//='])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['**'])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['//'])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['+='])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['-='])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['*='])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['/='])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['%='])+'S'==code:
				arith_op_count+=1
			elif str(SYM_CODE['='])+'S'==code:  #这个是赋值操作检测
				value_assign_count+=1
	weight_keys_list=list(def_weights.keys())
	#count_list=[func_count,judgement_stru_count,loop_stru_count,
	#	error_handle_count,arith_count,value_assign_count]
	#i=0
	#for ele in def_weights:
	#	if i>1:
	#		result[ele]=count_list[i]
	#	i+=1
	result={weight_keys_list[2]:func_count,
		 weight_keys_list[3]:judgement_stru_count,
		 weight_keys_list[4]:loop_stru_count,
		 weight_keys_list[5]:error_handle_count,
		 weight_keys_list[6]:arith_op_count,
		 weight_keys_list[7]:value_assign_count
		 }
	return result

#def extract_function_info(file_content):
#	function_name_list=[]
#	for line in file_content:
#		code_list=line.split(' ')
#		if str(KEY_CODE['def'])+'K' in code_list:
#			function_name_list.append(code_list[code_list.index(str(KEY_CODE['def'])+'K')+1])
#			#try:
#			#	function_args_index_start=code_list.index(str(SYM_CODE['(']+'S'))+1
#			#	fucntion_args_index_end=code_list.index(str(SYM_CODE[')']+'S'))
#			#except:
#			#	print('function args not found')
#			#	function_args_index_start=fucntion_args_index_end=-1
#			#if function_args_index_start!=-1:
#			#	i=function_args_index_start
#			#	function_args=[]
#			#	while i<fucntion_args_index_end:
#			#		function_args.append(code_list[i])
#			#		i+=1
#			#else:
#			#	pass
#			this_function_index

#def extract_functions(encoded_file_content):
#	function_list=[]
#	for line in file_content:
#		code_list=line[1].split(' ')
#		if str(KEY_CODE['def'])+'K' in code_list:
#			function_list.append(code_list[code_list.index(str(KEY_CODE['def'])+'K')+1])
#	return function_list


#function_list=extract_function(file_content)
#function_connection_graph={}
#def function_connect(encoded_file_content,current_line_index,current_function):
#	if len(function_list)==0:
#		pass
#	else:
#		i=current_line_index
#		toplevel=encoded_file_content[current_line_index][0]
#		while i<len(encoded_file_content):
#			line=encoded_file_content[i]
#			if line[0]<toplevel:
#				return
#			else:
#				code_list=line[1].split(' ')
#				this_line_functions=[]
#				for code in code_list:
#					if code in function_list:
#						this_line_functions.append(code)
#				if str(KEY_CODE['def'])+'K' in code_list:
#					if code_list.index(str(KEY_CODE['def'])+'K')==line[0]:

#					current_function=code_list[code_list.index(str(KEY_CODE['def'])+'K')+1]
#					#current_tab_level=line[0]
#					this_line_functions.remove(current_function)
#				for function in this_line_functions:
#					if current_function not in function_connection_graph:
#						function_connection_graph[current_function]=this_line_functions
#					else:
#						for connected_function in function_connection_graph[current_function]:
#							this_line_functions.remove(connected_function)
#						function_connection_graph[current_function]+=this_line_functions
#			i+=1
#暂时废弃通过函数调用图计算相似度，有如下问题：
#1. 缺少语法和语义分析很难正确提取出调用的函数名称。比如以下这个套娃函数：
#def functionA(functionC,str=functionA(1)):
#	print('functionA()')
#	def functionB():
#		print('functionB')
#		def functionC():print('functionC')
#		functionC()
#	functionB()
#但也许可以用var(的模式识别，有def就是定义，没有就是调用
#2. 图的相似度计算，SIM_RANK算法？