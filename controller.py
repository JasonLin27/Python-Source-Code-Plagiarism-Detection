from basic_info import def_weights,error_definition,weights_name
from file_access import output_to_csv,walk_through,read_file
from string_comparison import string_comparison
from properties_comparison import properties_comp
from code_simplify import Simplifyer
from cmd_mode import CMD_Mode
from GUI_mode import App_UI,GUI_available

class Controller:
	def __init__(self):
		self.simplfier_instance=Simplifyer(self)
		self.cmd_interface=CMD_Mode(self)
		self.GUI_interface=App_UI(self)

	#custom_args为对比函数附加参数，见各对比函数的参数
	#comp_method直接由上一级函数判定真实函数名后做参数传入
	def comp(self,source_folder,custom_args,comp_method):
		status=True
		comp_result=[]
		if comp_method is properties_comp:
			if len(custom_args)==0:
				custom_args=def_weights
			elif len(custom_args)!=len(def_weights):
				status=error_definition['CUSTOM_ARGS_ERROR']
		elif comp_method is string_comparison:
			if custom_args not in [1,2]:
				status=error_definition['CUSTOM_ARGS_ERROR']
		else:
			status=error_definition['INVALID_FUNCTION_NAME']
		files=walk_through(source_folder)
		if len(files)==0:
			status=error_definition['NO_SOURCE_FILES_ERROR']
		elif len(files)==1:
			status=error_definition['SOURCE_FILE_NOT_ENOUGH_ERROR']
		elif status==True:
			simplified_content_list=[]
			for file in files:
				simplify_res=self.simplfier_instance.getSimplyfiedRes(file)
				sim_status=simplify_res['status']
				if sim_status!=True:
					status=sim_status
					print('Simplify ERR:'+file)
					break
				else:
					simplified_content_list.append(simplify_res['result'])
			if status==True and len(simplified_content_list)>1:
				file_1_index=file_2_index=0
				for file_content_1 in simplified_content_list:
					single_file_result=[]
					file_2_index=0
					for file_content_2 in simplified_content_list:
						if file_1_index==file_2_index:
							file_2_index+=1
							continue
						else:
							#simplify_res_1=self.simplfier_instance.getSimplyfiedRes(file_1)
							#simplify_res_2=self.simplfier_instance.getSimplyfiedRes(file_2)
							#sim_status_1=simplify_res_1['status']
							#sim_status_2=simplify_res_2['status']
							#if sim_status_1!=True:
							#	status=sim_status_1
							#	print('Simplify ERR:'+file_1)
							#	break
							#elif sim_status_2!=True:
							#	status=sim_status_2
							#	print('Simplify ERR:'+file_2)
							#	break
							#else:
								#file_content1=simplify_res_1['result']
								#file_content2=simplify_res_2['result']
							temp=comp_method(file_content_1,file_content_2,custom_args)
							if temp['status']==True:
								single_file_result.append(temp['result'])
								status=True
								file_2_index+=1
							else:
								print('Error Related Files:\n'+files[file_1_index]+'\n'+files[file_2_index])
								status=temp['status']
								break
					if status==True:
						comp_result.append(single_file_result)
						status=True
						file_1_index+=1
					else:
						break
			elif status==True:
				status=error_definition['SOURCE_FILE_NOT_ENOUGH_ERROR']
			else:
				pass
		return {'status':status,'result':comp_result,'file_list':files}

	def read_file_proxy(self,filepath):
		return read_file(filepath)

	def output_to_csv_proxy(self,result_matrix,files_path_info,save_filepath):
		return output_to_csv(result_matrix,files_path_info,save_filepath)

	def launch(self):
		global GUI_available
		if GUI_available==False:
			print('Import tkinter failed. GUI is unavailable.')
			self.cmd_interface.cmd_start()
		else:
			interface_select=input("Press C then enter to disable GUI mode\nOr press other keys then enter to enable GUI mode\n")
			if interface_select in ['c','C']:
				self.cmd_interface.cmd_start()
			else:
				self.GUI_interface.ui_start()

	#def get_CODE(self):
	#	return KEY_CODE

	#def get_CONST_CODE(self):
	#	return CONST_CODE

	#def get_VAR_CODE(self):
	#	return VAR_CODE

	#def get_digitset(self):
	#	return {'bindigit':bindigit}
