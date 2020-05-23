import os
from basic_info import error_definition

fileSuffix=['py','Py','pY','PY']

def walk_through(dirname):	#遍历指定目录下所有文件
	result = []#所有的文件
	for maindir, subdir, file_name_list in os.walk(dirname,topdown=False):  #topdown控制遍历当前目录(True)还是子目录
		#print("1:",maindir) #当前主目录
		#print("2:",subdir) #当前主目录下的所有目录
		#print("3:",file_name_list)	#当前主目录下的所有文件
		for filename in file_name_list:
			apath = os.path.join(maindir, filename)#合并成一个完整路径
			ext = os.path.splitext(apath)[1][1:]  # [1]获取文件后缀，[1:]是去除.适配fileSuffix
			if ext in fileSuffix:  #过滤文件类型，符合的才加到结果集中
				result.append(apath)
	return result

def read_file(path):  #读取指定路径的文件内容。以列表形式返回，一行一列
	fileSuffixErrCount=0
	for suffix in fileSuffix:
		if path.endswith(suffix):
			fileSuffixErrCount+=1
	if fileSuffixErrCount==len(fileSuffix):
		#print("错误：不是python源代码文件")
		status=error_definition['INVALID_FILE_TYPE']
		result=[]
	try:
		file=open(path,'r',encoding='utf-8')
		content=[line.rstrip() for line in file]
		#for ele in content:
		#	print(ele,end='')
		#print('\n')
		result=content
		status=True
		file.close()
	except:
		#print("打开文件失败")
		status=error_definition['FILE_ACCESS_FAILED']
		result=[]
	return {'status':status,'result':result}
	
def output_to_csv(result_matrix,files_path_info,save_filepath):
	try:
		outfile=open(save_filepath,'w')
	except:
		status=error_definition['FILE_SAVE_ERROR']
	else:
		column=row=0
		outfile.write(',')
		for filepath in files_path_info:
			if filepath.rfind('\\')>filepath.rfind('/'):
				slash_index=filepath.rfind('\\')
			else:
				slash_index=filepath.rfind('/')
			outfile.write(filepath[slash_index+1:filepath.rfind('.')]+',')
			#outfile.write(filepath+',')
		outfile.write('\n')
		for single_file_result in result_matrix:
			if files_path_info[row].rfind('\\')>files_path_info[row].rfind('/'):
				slash_index=files_path_info[row].rfind('\\')
			else:
				slash_index=files_path_info[row].rfind('/')
			outfile.write(files_path_info[row][slash_index+1:files_path_info[row].rfind('.')]+',')
			#outfile.write(filepath+',')
			for single_result in single_file_result:
				if column==row:
					outfile.write(',')
					column+=1
				outfile.write(str(single_result)+',')
				column+=1
			row+=1
			column=0
			outfile.write('\n')
		status=True
		outfile.close()
	return status
