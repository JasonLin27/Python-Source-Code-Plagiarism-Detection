from basic_info import error_definition

class Simplifyer:  #Remove annotation and empty line  （Annotation Remove Disabled)
	def __init__(self,controller):
		self.controllerRef=controller
		self.fileSuffix=['py','Py','pY','PY']
		self.file=''
		self.error_status=True
		self.fileContent=[]
		self.simplyfiedRes=[]

	def set_target_file(self,filepath):
		self.file=filepath

	def __read_file(self):
		res=self.controllerRef.read_file_proxy(self.file)
		if res['status']==True:
			return res['result']
		else:
			self.error_status=res['status']
			return []

	def __simplyfy(self):
		if len(self.fileContent)==0:
			#self.error_status=error_definition['FILE_ACCESS_FAILED']
			return []
		else:
			i=0  #使用i而不是用for的原因是：for遍历实际上存在一个游标，
				 #而遍历过程中移除列表项游标不会变化，造成移除后直接跳过了移除项的下一项
			while i<len(self.fileContent):
				line=self.fileContent[i] 
				originLine=line
				#str='//#'#test					#TODO:正确识别#注释和引号混合；识别多行注释"""111"""；
				#while '#' in line:             #SOLVED:在词法识别过程中解决
				#	line=line[:line.rfind('#')]
				line=line.rstrip()  #Remove space and tab in the end at the same time
				if len(line)==0:
					self.fileContent.remove(originLine)
				elif line[-1]=='\\':  #将反斜杠的多行合并为1行
					i2=i
					while self.fileContent[i2][-1]=='\\' and i2<len(self.fileContent):
						if i2==i:
							line=line[:-1]
						else:
							line+=self.fileContent[i2][:-1].lstrip()
							self.fileContent[i2]=''
						i2+=1
					self.fileContent[self.fileContent.index(originLine)]=line+self.fileContent[i2].lstrip()
					self.fileContent[i2]=''
					i+=1
				else:
					self.fileContent[self.fileContent.index(originLine)]=line
					i+=1
		return self.fileContent
		#Notice: Shouldn't delete space and tab in the left of line since that wil break the structure of the code.

	#def isall(self,substr,str): #find out whether str is full of substr
	#	if len(str)==len(substr)*str.count(substr):
	#		return True
	#	else:
	#		return False #Warning: May cause security breach

	def getSimplyfiedRes(self,target_file):
		self.set_target_file(target_file)
		self.error_status=True
		self.fileContent=self.__read_file()
		self.simplyfiedRes=self.__simplyfy()
		return {'result':self.simplyfiedRes,'status':self.error_status}
