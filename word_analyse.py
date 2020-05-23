from basic_info import *

class Word_Analyser:
	def __init__(self,content):  #content要求格式为将文件内容一行作为一个元素放在列表中
		self.file_content=content  #待分析的文件内容，作为初始化类时输入的参数。
		self.trans_content=[]  #词法分析后文件内容
		self.temp_string=''  #凑词用临时字符串
		self.line_trans_content=''  #转码后的行内容
		self.var_list=[]  #变量列表
		self.const_list=[]  #常量列表
		self.ano_list=[]  #注释列表
		#下面为标志全局变量
		self.TRANS_TYPE_STRING=0  #type=0为字符串，1为符号，2为数字，3为关键字或变量名，4为注释
		self.TRANS_TYPE_SYMBLE=1
		self.TRANS_TYPE_NUM=2
		self.TRANS_TYPE_KEY_OR_VAR=3
		self.TRANS_TYPE_ANO=4
		self.QUOTE_NOT_IN_PAIR=10  #代表无待配对三连引号
		self.QUOTE_IN_PAIR_SINGLE=11  #代表三连单引号跨行待配对
		self.QUOTE_IN_PAIR_DOUBLE=12  #代表三连双引号跨行待配对
		self.INTEGER_TYPE_NORMAL=21  #数字类型：普通整型
		self.INTEGER_TYPE_BIN=22  #数字类型：二进制整型
		self.INTEGER_TYPE_OCT=23  #数字类型：8进制整型
		self.INTEGER_TYPE_HEX=24  #数字类型：16进制整型
		self.FLOAT_TYPE=25  #数字类型：浮点
		self.COMPLEX_TYPE=26  #数字类型：复数
		#下面是标志位
		self.normal_crossline=False  #反斜杠跨行标志位
		self.analyse_status=True  #分析成功标记
		self.status=0  #状态码1：0代表正在凑词，>0代表正在进行括号配对/跨行处理
		self.par_status=self.QUOTE_NOT_IN_PAIR  #状态码2，状态为QUOTE_NOT_IN_PAIR 和 QUOTE_IN_PAIR

	def word_analyse(self):
		for line in self.file_content:
			if self.status==0 and self.normal_crossline==False and self.par_status==self.QUOTE_NOT_IN_PAIR:
				#self.trans_content.append(self.line_trans_content)
				self.line_trans_content=''
			tab_level=0  #缩进量
			start=0  #凑词开始指针
			end=start  #凑词结束指针
			while end<len(line):
				#start=end=0
				self.temp_string+=line[end]
				if self.par_status in [self.QUOTE_IN_PAIR_SINGLE,self.QUOTE_IN_PAIR_DOUBLE]:
					if self.par_status==self.QUOTE_IN_PAIR_SINGLE:
						quote="'"
					elif self.par_status==self.QUOTE_IN_PAIR_DOUBLE:
						quote='"'
					else:
						#print("QUOTE_IN_PAIR_STATUS_CODE_ERROR")
						self.analyse_status=error_definition['LEXICAL_ANALYSIS_INVALID_PAIR_STATUS']
						break
					if end+2<len(line) and line[end]==line[end+1]==line[end+2]==quote:
						self.trans_string(self.temp_string[:-1],self.TRANS_TYPE_STRING)
						self.par_status=self.QUOTE_NOT_IN_PAIR
						self.trans_string(quote*3,self.TRANS_TYPE_SYMBLE)
						start=end=end+3
						self.temp_string=''
					else:
						if end+1==len(line):
							self.temp_string+='\n'
						end+=1
				elif self.par_status==self.QUOTE_NOT_IN_PAIR:
					#if end==len(line)-1:
					#	if line[end] in ['\t',' ']:
					#		temp_string=''
					#		continue
					#	elif line[end]=='':
					#		self.trans_string(temp_string,self.TRANS_TYPE_SYMBLE,line_trans_content)
					#		start=end=end+1
					if line[end]=='\\' and end==len(line)-1:
						self.normal_crossline=True
						end+=1
						continue
					if line[end]=='\t':
						if end+1<len(line) and line[end+1]!='\t':
							if start==0:
								tab_level=len(self.temp_string)
							else:
								pass  #凑词结束（连续非行开头tab忽略，因为其他元素转码末尾自带空格）
							start=end=end+1
							self.temp_string=''
						else:
							end+=1
					elif line[end]==' ':
						if end+1<len(line) and line[end+1]!=' ':
							if start==0:
								if len(self.temp_string)%4!=0:
									self.analyse_status=error_definition['LEXICAL_ANALYSIS_INCONSISTENT_TAB']
									break
								else:
									tab_level=int(len(self.temp_string)/4)
							else:
								pass  #凑词结束（连续非行开头空格忽略，同上）
							start=end=end+1
							self.temp_string=''
						else:
							end+=1
					elif line[end] in ['~' , '^' , '|' , '&','@',',',':']:
						self.trans_string(line[end],self.TRANS_TYPE_SYMBLE)
						self.temp_string=''
						start=end=end+1  #凑词结束（用对应符号码替换）
					elif line[end] in ['*','/']:
						if end+1<len(line) and line[end+1]==line[end]:
							if self.temp_string==2*line[end]:
								self.trans_string(self.temp_string,self.TRANS_TYPE_SYMBLE)
								self.temp_string=line[end+1]
								start=end=end+2
							elif self.temp_string==line[end]:
								if end+2<len(line) and line[end+2]=='=':
									self.trans_string(self.temp_string+line[end+1:end+3],self.TRANS_TYPE_SYMBLE)
									self.temp_string=''
									start=end=end+3
								else:
									self.trans_string(self.temp_string+line[end+1],self.TRANS_TYPE_SYMBLE)
									self.temp_string=''
									start=end=end+2
						elif end+1<len(line) and line[end+1]=='=':
							self.trans_string(self.temp_string+line[end+1],self.TRANS_TYPE_SYMBLE)
							self.temp_string=''
							start=end=end+2
						else:
							self.trans_string(self.temp_string,self.TRANS_TYPE_SYMBLE)
							self.temp_string=''
							start=end=end+1  #凑词结束（用对应符号码替换）
					elif line[end] in ['+' , '-' , '%']:
						if end+1<len(line) and line[end+1]=='=':
							self.trans_string(self.temp_string+line[end+1],self.TRANS_TYPE_SYMBLE)
							self.temp_string=''
							start=end=end+2
						#elif line[end]!='%' and (self.is_single_digit(line[end+1])==True or line[end+1]=='.'):
						#	self.temp_string+=line[end+1]
						#	start=end=end+2
						else:
							self.trans_string(self.temp_string,self.TRANS_TYPE_SYMBLE)
							self.temp_string=''
							end+=1
					elif line[end] in ['(','[','{',]:
						self.status+=1
						self.trans_string(line[end],self.TRANS_TYPE_SYMBLE)
						self.temp_string=''
						start=end=end+1
					elif line[end]in [')',']','}']:
						self.status-=1
						self.trans_string(line[end],self.TRANS_TYPE_SYMBLE)
						self.temp_string=''
						start=end=end+1
					elif line[end]=='<':
						if end+1<len(line) and (line[end+1]in ['<','=','>']):
							self.trans_string(self.temp_string+line[end+1],self.TRANS_TYPE_SYMBLE)
							start=end=end+2
						else:
							self.trans_string(self.temp_string,self.TRANS_TYPE_SYMBLE)
							start=end=end+1
						self.temp_string=''
					elif line[end]=='>':
						if end+1<len(line) and (line[end+1] in ['>','=']):
							self.trans_string(self.temp_string+line[end+1],self.TRANS_TYPE_SYMBLE)
							start=end=end+2
						else:
							self.trans_string(self.temp_string,self.TRANS_TYPE_SYMBLE)
							start=end=end+1
						self.temp_string=''
					elif line[end] in ['!','=']:
						if end+1<len(line) and line[end+1]=='=':
							self.trans_string(self.temp_string+line[end+1],self.TRANS_TYPE_SYMBLE)
							start=end=end+2
						else:
							self.trans_string(self.temp_string,self.TRANS_TYPE_SYMBLE)
							start=end=end+1
						self.temp_string=''
					#elif line[end]=='=':
					#	if end+1<len(line) and line[end+1]=='=':
					#		self.trans_string(self.temp_string+line[end+1],self.TRANS_TYPE_SYMBLE)
					#		start=end=end+2
					#	else:
					#		self.trans_string(self.temp_string,self.TRANS_TYPE_SYMBLE)
					#		start=end=end+1
					#	self.temp_string=''
					elif line[end]=='.' :
						if end+1<len(line) and self.is_single_digit(line[end+1])==True:
							end+=1
						else:
							self.trans_string(self.temp_string,self.TRANS_TYPE_SYMBLE)
							self.temp_string=''
							start=end=end+1
					elif line[end]=='#':
						self.temp_string=line[end+1:]
						self.trans_string(self.temp_string,self.TRANS_TYPE_ANO)
						end=len(line)
						self.temp_string=''
						continue
					elif line[end] in ["'" ,'"']:
						quote=line[end]
						if end+2<len(line) and line[end+2]==line[end+1]==quote:
							if self.par_status==self.QUOTE_NOT_IN_PAIR:
								if quote=="'":
									self.par_status=self.QUOTE_IN_PAIR_SINGLE
								else:
									self.par_status=self.QUOTE_IN_PAIR_DOUBLE
								self.trans_string(quote*3,self.TRANS_TYPE_SYMBLE)
								self.temp_string=''
								start=end=end+3
						else:
							self.trans_string(line[end],self.TRANS_TYPE_SYMBLE)
							start=end+1
							end=line[start:].find(quote)+end+1
							if end<start:  #当无法在剩下的字符串中找到引号的end值==start-1
								self.analyse_status=error_definition['LEXICAL_ANALYSIS_QUOTE_NOT_IN_PAIR']
								break
							else:
								self.temp_string=line[start:end]
								self.trans_string(self.temp_string,self.TRANS_TYPE_STRING)
								self.temp_string=line[end]  #不重置tempstring会导致符号转换500错误
								self.trans_string(line[end],self.TRANS_TYPE_SYMBLE)
								#self.par_status=self.QUOTE_NOT_IN_PAIR
								start=end=end+1
							self.temp_string=''
					elif self.is_single_letter(line[end])==True or line[end]=='_':
						if end+1<len(line) and (self.is_single_letter(line[end+1])==True \
							or self.is_single_digit(line[end+1])==True or line[end+1] in ['_']):
							end+=1
						else:
							self.trans_string(self.temp_string,self.TRANS_TYPE_KEY_OR_VAR)
							start=end=end+1
							self.temp_string=''
					elif self.is_single_digit(line[end])==True:
						process_result=self.digit_processing(line,self.temp_string,start,end)
						if process_result['success_flag']==True:
							start=end=process_result['end']+1
							self.temp_string=''
						else:
							#有可能为变量名称
							if end+1<len(line) and (self.is_single_letter(line[end+1])==True \
								or self.is_single_digit(line[end+1])==True or line[end+1] in ['_']):
								end+=1
							else:
								self.trans_string(self.temp_string,self.TRANS_TYPE_KEY_OR_VAR)
								start=end=end+1
								self.temp_string=''
							#self.analyse_status=False
							#break
					else:
						end+=1  #遇到未知符号时读取下一个
				else:
					self.analyse_status=error_definition['LEXICAL_ANALYSIS_INVALID_PAIR_STATUS']
					break
			if self.analyse_status!=True:
				break
			elif len(self.line_trans_content)>0 and self.status==0 and self.par_status==self.QUOTE_NOT_IN_PAIR:
				self.trans_content.append([tab_level,self.line_trans_content])
			

	def trans_string(self,untrans_str,type):  #转换字符串untrans_str为码并与transed_str结合
		#flag=False
		if type==self.TRANS_TYPE_STRING:
			#if untrans_str in self.const_list:
			#	code=self.const_list.index(untrans_str)+CONST_CODE
			#else:
			#	self.const_list.append(untrans_str)
			#	code=len(self.const_list)+CONST_CODE
			self.const_list.append(untrans_str)  #对于字符串或数字等常量不需要查重
			code=str(len(self.const_list)+CONST_CODE)+TYPE_CODE['const']  #注意code的生成和list.append的顺序对code的值有影响，因此需要保持操作顺序一致
			#flag=True
		elif type==self.TRANS_TYPE_SYMBLE:
			try:
				code=str(SYM_CODE[untrans_str])+TYPE_CODE['sym']
			except KeyError:
				code=str(ERROR_CODE)+TYPE_CODE['err']
				self.analyse_status=error_definition['LEXICAL_ANALYSIS_INVALID_CHAR']
		elif type in [self.INTEGER_TYPE_NORMAL,self.INTEGER_TYPE_BIN,self.INTEGER_TYPE_OCT,self.INTEGER_TYPE_HEX]:
			#if int(untrans_str) in self.const_list:
			#	code=self.const_list.index(int(untrans_str))+CONST_CODE
			#else:
			#	code=len(self.const_list)+CONST_CODE
			#	self.const_list.append(int(untrans_str))
			if type==self.INTEGER_TYPE_NORMAL:
				self.const_list.append(int(untrans_str))
			elif type==self.INTEGER_TYPE_BIN:
				self.const_list.append(int(untrans_str,2))
			elif type==self.INTEGER_TYPE_OCT:
				self.const_list.append(int(untrans_str,8))
			elif type==self.INTEGER_TYPE_HEX:
				self.const_list.append(int(untrans_str,16))
			code=str(len(self.const_list)+CONST_CODE)+TYPE_CODE['const']
		elif type==self.FLOAT_TYPE:
			try:
				self.const_list.append(float(untrans_str))
				code=str(len(self.const_list)+CONST_CODE)+TYPE_CODE['const']
			except:
				code=str(ERROR_CODE)+TYPE_CODE['err']
				self.analyse_status=error_definition['LEXICAL_ANALYSIS_FLOAT_FORMAT_ERROR']
		elif type==self.COMPLEX_TYPE:
			if 'j' in untrans_str or 'J' in untrans_str:
				if 'j' in untrans_str:
					mark='j'
				else:
					mark='J'
				if '+' in untrans_str:
					self.const_list.append(complex(float(untrans_str[:untrans_str.find('+')]),float(untrans_str[:untrans_str.find(mark)])))
				elif '-' in untrans_str:
					self.const_list.append(complex(float(untrans_str[:untrans_str.find('-')]),float(untrans_str[:untrans_str.find(mark)])))
				else:
					self.const_list.append(complex(0,float(untrans_str[:untrans_str.find(mark)])))
				code=str(len(self.const_list)+CONST_CODE)+TYPE_CODE['const']
			else:
				print("尝试转换属于复数的字符串中没有符号j/J")
				code=str(ERROR_CODE)+TYPE_CODE['err']
				self.analyse_status='LEXICAL_ANALYSIS_COMPLEX_FORMAT_ERROR'
		elif type==self.TRANS_TYPE_KEY_OR_VAR:
			try:
				code=str(KEY_CODE[untrans_str])+TYPE_CODE['key']
			except KeyError:
				for ch in untrans_str:
					if self.is_single_letter(ch)==False and self.is_single_digit(ch)==False and ch!='_':
						code=str(ERROR_CODE)+TYPE_CODE['err']
						self.analyse_status=error_definition['LEXICAL_ANALYSIS_INVALID_CHAR']
						#print('变量名称出现非法字符')
						break
				if self.is_single_letter(untrans_str[0])==False and untrans_str[0]!='_':
					code=str(ERROR_CODE)+TYPE_CODE['err']
					self.analyse_status=error_definition['LEXICAL_ANALYSIS_INVALID_VARIABLE_NAME']
					#print('变量名称不合法')
				if untrans_str in self.var_list:
					code=str(self.var_list.index(untrans_str)+VAR_CODE+1)+TYPE_CODE['var']  #这里的查重从语义角度有误，因为无法区分全局和局部变量
				else:
					self.var_list.append(untrans_str)  #当后续接入语义分析时需关闭此查重
					code=str(len(self.var_list)+VAR_CODE)+TYPE_CODE['var']
				#flag=True
		elif type==self.TRANS_TYPE_ANO:
			self.ano_list.append(untrans_str)
			code=str(len(self.ano_list)+ANO_CODE)+TYPE_CODE['ano']
			#flag=True
		else:
			print('传入参数type错误')
			code=str(ERROR_CODE)+TYPE_CODE['err']
			self.analyse_status=error_definition['LEXICAL_ANALYSIS_INVALID_FUNCTION_ARGS']
		#self.line_trans_content+=str(code)+' '
		self.line_trans_content+=code+' '

	def is_single_digit(self,ch):  #判断是否为单一数字
		if len(ch)>1:
			return False
		else:
			return ch.isdigit()

	def is_single_letter(self,ch):  #判断是否为单一字母
		if len(ch)>1:
			return False
		else:
			return ch.isalpha()

	def get_result(self):  #获取分析结果
		self.word_analyse()
		return {'status':self.analyse_status,'vars':self.var_list,'consts':self.const_list,'annos':self.ano_list,'trans_content':self.trans_content}

	def digit_processing(self,line,temp_string,start,end):
		succeed=False
		if len(temp_string)>0:
			if end+1==len(line):  #end为该行最后一个字符时
				process_string=temp_string  #只需要处理temp_string
				#digit_start=end-len(temp_string)+1
			else:
				process_string=temp_string+line[end+1:]  #否则需要合并temp_string和该行剩余的内容
			digit_start=end-len(temp_string)+1  #数字识别在行中的开始位置
		elif end<len(line):
			process_string=line[end:]
			digit_start=end
		else:
			print("数字处理准备字段错误")
			digit_start=end
			succeed=False
		integer_result=self.integer_process(process_string)
		floatpoint_result=self.float_process(process_string)
		complex_result=self.complex_process(process_string)
		if integer_result['is_integer']==True:
			if floatpoint_result['is_float']==True:
				if complex_result['is_complex']==True:
					if len(integer_result['data'])>len(floatpoint_result['data']):
						if len(integer_result['data'])>len(complex_result['data']):
							valid_result=integer_result							
						else:
							valid_result=complex_result
					else:
						if len(floatpoint_result['data'])>len(complex_result['data']):
							valid_result=floatpoint_result
						else:
							valid_result=complex_result
				else:
					if len(integer_result['data'])>len(floatpoint_result['data']):
						valid_result=integer_result
					else:
						valid_result=floatpoint_result
			else:
				if complex_result['is_complex']==True:
					if len(integer_result['data'])>len(complex_result['data']):
						valid_result=integer_result
					else:
						valid_result=complex_result
				else:
					valid_result=integer_result
		else:
			if floatpoint_result['is_float']==True:
				if complex_result['is_complex']==True:
					if len(floatpoint_result['data'])>len(complex_result['data']):
						valid_result=floatpoint_result
					else:
						valid_result=complex_result
				else:
					valid_result=floatpoint_result
			else:
				if complex_result['is_complex']==True:
					valid_result=complex_result
				else:
					valid_result={}
		if len(valid_result)!=0:
			new_end=digit_start+valid_result['move']-1
			if new_end+1<len(line) and self.is_single_letter(line[new_end+1])==True:
				succeed=False
				new_end=end
			else:
				succeed=True
				self.trans_string(valid_result['data'],valid_result['type'])
		else:
			new_end=end
		return {'success_flag':succeed,'end':new_end}

	def integer_process(self,untrans_str):
		substatus=0  #状态编号
		i=0  #字符串游标
		is_integer=False
		while i<len(untrans_str):
			if substatus==0:
				if untrans_str[i] in nonzerodigit:
					substatus=1
					i+=1
				elif untrans_str[i]=='0':
					substatus=2
					i+=1
				else:
					is_integer=False
					break
			elif substatus==1:
				if untrans_str[i]=='_':
					substatus=3
					i+=1
				elif untrans_str[i] in digit:
					substatus=5
					i+=1
				else:
					is_integer==True
					i-=1
					break
			elif substatus==2:
				if untrans_str[i]=='0': #and substatus==2:
					substatus=5
					i+=1
				elif untrans_str[i] in ['b','B']:
					substatus=7
					i+=1
				elif untrans_str[i] in ['o','O']:
					substatus=8
					i+=1
				elif untrans_str[i] in ['x','X']:
					substatus=9
					i+=1
				else:
					is_integer==True
					i-=1
					break
			elif substatus==3:
				if untrans_str[i] in digit:
					substatus=4
					i+=1
				else:
					is_integer=False
					break
			elif substatus==4:
				if untrans_str[i] in digit:
					#substatus=4
					i+=1
				elif untrans_str[i]=='_':
					substatus=3
					i+=1
				else:
					is_integer==True
					i-=1
					break
			elif substatus==5:
				if untrans_str[i]=='0':
					#substatus=5
					i+=1
				elif untrans_str[i]=='_':
					substatus=6
					i+=1
				else:
					is_integer=True
					i-=1
					break
			elif substatus==6:
				if untrans_str[i]=='0':
					substatus=5
					i+=1
				else:
					is_integer=False
					break
			elif substatus in [7,8,9]:
				if substatus==7:
					digit_set=bindigit
				elif substatus==8:
					digit_set=octdigit
				else:
					digit_set=hexdigit
				if untrans_str[i]=='_':
					substatus=substatus+3
					i+=1
				elif untrans_str[i] in digit_set:
					substatus=substatus+6
				else:
					is_integer=False
					break
			elif substatus in [10,11,12]:
				if substatus==10:
					digit_set=bindigit
				elif substatus==11:
					digit_set=octdigit
				else:
					digit_set=hexdigit
				if untrans_str[i] in digit_set:
					substatus=substatus+3
				else:
					is_integer=False
					break
			elif substatus in [13,14,15]:
				if substatus==13:
					digit_set=bindigit
				elif substatus==14:
					digit_set=octdigit
				else:
					digit_set=hexdigit
				if untrans_str[i] in digit_set:
					#substatus=substatus
					i+=1
				elif untrans_str[i]=='_':
					substatus=substatus-3
					i+=1
				else:
					is_integer=True
					i-=1
					break
		data=untrans_str[:i+1]
		if substatus in [1,2,4,5]:
			data_type=self.INTEGER_TYPE_NORMAL
			is_integer=True
		elif substatus==13:
			data_type=self.INTEGER_TYPE_BIN
			is_integer=True
		elif substatus==14:
			data_type=self.INTEGER_TYPE_OCT
			is_integer=True
		elif substatus==15:
			data_type=self.INTEGER_TYPE_HEX
			is_integer=True
		else:
			data_type=-1
		result={'is_integer':is_integer,'data':data,'type':data_type,'move':len(data)}
		return result

	def float_process(self,untrans_str):
		substatus=0  #状态编号
		i=0  #字符串游标
		is_float=False
		while i<len(untrans_str):
			if substatus==0:
				if untrans_str[i] in digit:
					substatus=1
					i+=1
				elif untrans_str[i]=='.':
					substatus=2
					i+=1
				else:
					is_float=False
					break
			elif substatus==1:
				if untrans_str[i] in digit:
					substatus=4
					i+=1
				elif untrans_str[i]=='_':
					substatus=3
					i+=1
				elif untrans_str[i] in ['e','E']:
					substatus=6
					i+=1
				elif untrans_str[i]=='.':
					substatus=5
					i+=1
				else:
					is_float==True
					i-=1
					break
			elif substatus==2:
				if untrans_str[i] in digit:
					substatus=5
				else:
					is_float=False
					break
			elif substatus==3:
				if untrans_str[i] in digit:
					substatus=4
				else:
					is_float=False
					break
			elif substatus==4:
				if untrans_str[i] in digit:
					#substatus=4
					i+=1
				elif untrans_str[i]=='.':
					substatus=5
					i+=1
				elif untrans_str[i]=='_':
					substatus=3
					i+=1
				elif untrans_str[i] in ['e','E']:
					substatus=6
					i+=1
				else:
					is_float=True
					i-=1
					break
			elif substatus==5:
				if untrans_str[i] in digit:
					#substatus=5
					i+=1
				elif untrans_str[i] in ['e','E']:
					substatus=6
					i+=1
				elif untrans_str[i]=='_':
					substatus=11
					i+=1
				else:
					is_float=True
					i-=1
					break
			elif substatus==6:
				if untrans_str[i] in ['+','-']:
					substatus=8
					i+=1
				elif untrans_str[i] in digit:
					substatus=7
					i+=1
				else:
					is_float=False
					break
			elif substatus==7:
				if untrans_str[i] in digit:
					substatus=12
					i+=1
				elif untrans_str[i]=='_':
					substatus=10
					i+=1
				else:
					is_float=True
					i-=1
					break
			elif substatus==8:
				if untrans_str[i] in digit:
					substatus=7
				else:
					is_float=False
					break
			elif substatus==9:
				if untrans_str[i] in digit:
					#substatus='_'
					i+=1
				elif untrans_str[i]=='_':
					substatus=11
					i+=1
				else:
					is_float=True
					i-=1
					break
			elif substatus==10:
				if untrans_str[i] in digit:
					substatus=12
					i+=1
				else:
					is_float=False
					break
			elif substatus==11:
				if untrans_str[i] in digit:
					substatus=9
					i+=1
				else:
					is_float=False
					break
			elif substatus==12:
				if untrans_str[i] in digit:
					#substatus=12
					i+=1
				else:
					is_float=True
					i-=1
					break
		data=untrans_str[:i+1]
		if substatus in [1,4,5,7,9,12]:
			data_type=self.FLOAT_TYPE
			is_float=True
		else:
			data_type=-1
		result={'is_float':is_float,'data':data,'type':data_type,'move':len(data)}
		return result

	def complex_process(self,untrans_str):
		substatus=0  #状态编号
		i=0  #字符串游标
		is_complex=False
		while i<len(untrans_str):
			if substatus==0:
				if untrans_str[i] in digit:
					substatus=1
					i+=1
				elif untrans_str[i]=='.':
					substatus=2
					i+=1
				else:
					is_complex=False
					i-=1
					break
			elif substatus==1:
				if untrans_str[i] in digit:
					#substatus=1
					i+=1
				elif untrans_str[i] in ['e','E']:
					substatus=5
					i+=1
				elif untrans_str[i] in ['j','J']:
					substatus=12
					i+=1
				elif untrans_str[i]=='.':
					substatus=4
					i+=1
				elif untrans_str[i]=='_':
					substatus=3
					i+=1
				else:
					is_complex=False
					break
			elif substatus==2:
				if untrans_str[i] in digit:
					substatus=6
					i+=1
				else:
					is_complex=False
					break
			elif substatus==3:
				if untrans_str[i] in digit:
					substatus=1
					i+=1
				else:
					is_complex=False
					break
			elif substatus==4:
				if untrans_str[i] in digit:
					substatus=6
					i+=1
				elif untrans_str[i] =='.':
					substatus=5
					i+=1
				elif untrans_str[i] in ['j','J']:
					substatus=12
				else:
					is_complex=False
					break
			elif substatus==5:
				if untrans_str[i] in ['+','-']:
					substatus=7
					i+=1
				elif untrans_str[i] in digit:
					substatus=11
					i+=1
				else:
					is_complex=False
					break
			elif substatus==6:
				if untrans_str[i] in ['e','E']:
					substatus=5
					i+=1
				elif untrans_str[i] in ['j','J']:
					substatus=12
					i+=1
				elif untrans_str[i] in digit:
					substatus=9
					i+=1
				elif untrans_str[i]=='_':
					substatus=8
					i+=1
				else:
					is_complex=False
					break
			elif substatus==7:
				if untrans_str[i] in digit:
					substatus=11
					i+=1
				else:
					is_complex=False
					break
			elif substatus==8:
				if untrans_str[i] in digit:
					substatus=9
					i+=1
				else:
					is_complex=False
					break
			elif substatus==9:
				if untrans_str[i] in digit:
					#substatus=9
					i+=1
				elif untrans_str[i]=='_':
					substauts=8
					i+=1
				elif untrans_str[i] in ['J','j']:
					substatus=12
					i+=1
				elif untrans_str[i] in ['e','E']:
					substatus=5
					i+=1
				else:
					is_complex=False
					break
			elif substatus==10:
				if untrans_str[i] in digit:
					substatus=11
					i+=1
				else:
					is_complex=False
					break
			elif substatus==11:
				if untrans_str[i]=='_':
					substatus=10
					i+=1
				elif untrans_str[i] in ['j','J']:
					substatus=12
					i+=1
				elif untrans_str[i] in digit:
					#substatus=11
					i+=1
				else:
					is_complex=False
					break
			elif substatus==12:
				is_complex=True
				i-=1
				break
		data=untrans_str[:i+1]
		if substatus==12:
			data_type=self.COMPLEX_TYPE
			is_complex=True
		else:
			data_type=-1
		result={'is_complex':is_complex,'data':data,'type':data_type,'move':len(data)}
		return result