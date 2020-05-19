from properties_comparison import properties_comp
from string_comparison import string_comparison
from basic_info import def_weights,error_definition,weights_name,error_info

class CMD_Mode:
	def __init__(self,controller):
		self.controllerRef=controller

	def cmd_start(self):
		files_path=input('输入源码文件夹路径：')
		while len(files_path)==0 or ('\\' not in files_path and '/' not in files_path):
			if len(files_path)==0:
				print('错误：保存文件路径为空')
				files_path=input('输入源码文件夹路径：')
			elif '\\' not in files_path and '/' not in files_path:
				choice=self.select_input('文件路径可能不合法，要继续吗?',['继续','取消'])
				if choice==1:
					break
				else:
					files_path=input('输入源码文件夹路径：')
		method=self.select_input('选择算法：',['字符串比对','属性计数'])
		if method==1:
			custom_args=self.select_input('选择模式：',['普通','激进'])
		else:
			for w in def_weights:
				print('|'+weights_name[w]+'\t\t\t|'+str(def_weights[w]))
			#print('\n')
			#for w in def_weights:
			#	print('|'+str(def_weight[w]))
			print('\n')
			choice=self.select_input('默认特征权重如上，需要更改吗？',['是','否'])
			if choice==1:
				new_weights=self.new_weights_input()
				sum=0
				for w in new_weights:
					sum+=new_weights[w]
				while len(new_weights)!=len(def_weights) or sum!=1:
					print('输入权重参数有误，重新输入')
					sum=0
					new_weights=self.new_weights_input()
					for w in new_weights:
						sum+=new_weights[w]
				custom_args=new_weights
			else:
				custom_args=def_weights
		if method==1:
			comp_method=string_comparison
		else:
			comp_method=properties_comp
		print('运行中，请勿关闭窗口\n')
		comp_result=self.controllerRef.comp(files_path,custom_args,comp_method)
		if comp_result['status']==True:
			choice=self.select_input('选择输出方式？',['终端','保存为csv（可用excel等打开）'])
			if choice==1:
				self.output_to_term(comp_result['result'],comp_result['file_list'])
			else:
				outFileFolder=input("保存文件路径(具体到文件夹即可)：")
				while len(outFileFolder)==0 or ('\\' not in outFileFolder and '/' not in outFileFolder):
					if len(outFileFolder)==0:
						print('错误：保存文件路径为空')
						outFileFolder=input("保存文件路径(具体到文件夹即可)：")
					elif '\\' not in outFileFolder and '/' not in outFileFolder:
						choice=self.select_input('文件路径可能不合法，要继续吗?',['继续','取消'])
						if choice==1:
							break
						else:
							outFileFolder=input("保存文件路径(具体到文件夹即可)：")
				outFileName=input('文件名：')
				while len(outFileName)==0 or self.filename_check(outFileName)==False:
					if len(outFileName)==0:
						print('错误：保存文件路径为空')
					elif self.filename_check(outFileName)==False:
						print('错误：文件名不合法')
					outFileName=input("文件名：")
				csv_file=outFileFolder+'\\'+outFileName+'.csv'
				save_status=self.controllerRef.output_to_csv_proxy(comp_result['result'],comp_result['file_list'],csv_file)
				if save_status==True:
					print('csv文件已保存到：'+csv_file)
				else:
					print('失败：',end='')
					try:
						print(error_info[save_status])
					except:
						print('文件保存过程中出现未知错误')
		else:
			print('失败：',end='')
			try:
				print(error_info[comp_result['status']])
			#if comp_result['status']==error_definition['NO_SOURCE_FILES_ERROR']:
			#	print('没有找到源代码文件。可能文件类型有误或路径有误。')
			#elif comp_result['status']==error_definition['SOURCE_FILE_NOT_ENOUGH_ERROR']:
			#	print('源代码文件不足。')
			#elif comp_result['status']==error_definition['CUSTOM_ARGS_ERROR']:
			#	print('自定义参数错误')
			#elif comp_result['status']==:
			#	print('')
			#elif comp_result['status']==:
			#	print('')
			#elif comp_result['status']==:
			#	print('')
			#elif comp_result['status']==:
			#	print('')
			#elif comp_result['status']==:
			#	print('')
			#elif comp_result['status']==:
			#	print('')
			except:
				print('未知错误')

	def filename_check(self,filename):
		for banned_symble in ['/','\\',':','*','?','"','<','>','|']:
			if banned_symble in filename:
				return False
		return True

	def new_weights_input(self):
		new_weights={}
		for w in def_weights:
			new_weight=0
			valid=False
			while valid==False:
				try:
					new_weight=float(input(weights_name[w]+':'))
				except:
					print('输入内容不是浮点型')
					valid=False
				else:
					if new_weight<0 or new_weight>1:
						print('输入范围错误，请输入0-1之间的小数，如0.15代表15%')
						valid=False
					else:
						valid=True
			#while new_weight<0 or new_weight>1:
			#	print('输入范围错误，请输入0-1之间的小数，如0.15代表15%')
			#	try:
			#		new_weight=float(input(weights_name[w]+':'))
			#	except:
			#		print('输入内容不是浮点型')
			#		new_weight=float(input(weights_name[w]+':'))
			new_weights[w]=new_weight
		return new_weights

	def select_input(self,title,choices):  #分支选择的输入
		print(title)
		i=1
		for choice in choices:
			print('['+str(i)+'] '+choice)
			i+=1
		print('输入：',end='')
		try:
			entry=int(input())
		except:
			print('输入错误')
			entry=0
		while entry>i-1 or entry<1:
			print('输入错误')
			try:
				entry=int(input())
			except:
				print('输入错误')
		return entry

	def output_to_term(self,result_matrix,files):
		column=row=0
		print('\t',end='')
		for filepath in files:
			print(filepath[filepath.rfind('\\')+1:filepath.rfind('.')]+'\t',end='')
		print('\n')
		for single_file_result in result_matrix:
			column=0
			print(files[row][files[row].rfind('\\')+1:files[row].rfind('.')]+'\t',end='')
			for single_result in single_file_result:
				if column==row:
					print('\t',end='')
					column+=1
				print('%.2f'%single_result,end='')
				#print(str(single_result),end='')
				print('\t',end='')
				column+=1
			row+=1
			print('\n')
