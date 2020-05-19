from properties_comparison import properties_comp
from string_comparison import string_comparison
from basic_info import def_weights,error_definition,weights_name,error_info
try:
	import tkinter as tk
	import tkinter.messagebox
	from tkinter import filedialog
	GUI_available=True
except :
	GUI_available=False
	

class App_UI:
	def __init__(self,controller):
		global GUI_available
		if GUI_available==False:
			return
		self.controllerRef=controller

		self.CHECK_BOX_ON=0
		self.CHECK_BOX_OFF=1
		self.COMP_METHOD_STRING=2
		self.COMP_METHOD_PROPERTIES=3
		self.files_path='待输入'  #比对源码存放的文件夹路径
		self.save_file_name=''
		self.save_file_path='待输入'  #结果csv文件存放路径
		self.WINDOW_TITLE_NORMAL='代码相似度计算'
		self.WINDOW_TITLE_RUNNING='运行中，请勿关闭窗口！不必理会->'
		#self.custom_weight_check=self.CHECK_BOX_OFF

		self.column_single_width=4
		self.button_width=self.column_single_width*2
		self.entry_width_long=self.column_single_width*12
		self.entry_width_short=self.column_single_width*2
		self.label_width_long=self.column_single_width*6
		self.label_width_short=self.column_single_width*2
		self.radio_width=self.column_single_width*3
		self.scale_width=self.column_single_width*2
		self.scale_width_offset=6
		self.def_weight_column_offset=2
		#self.weight_label_width=10
		#self.weight_entry_width=10
		#self.comp_method_radio_width=150

		self.home_window=tk.Tk()
		self.filepath_entry_variable=tk.StringVar(self.home_window)
		self.save_file_entry_variable=tk.StringVar(self.home_window)
		self.save_name_entry_variable=tk.StringVar(self.home_window)
		self.comp_method=tk.IntVar(self.home_window)  #选择的比对算法，1为字符串比对，2为特征计数
		self.custom_weight_check=tk.IntVar(self.home_window)  #权重自定义checkbox状态

		#self.file_info_frame=tk.Frame(self.file_info_frame)  #注意frame应该是不能嵌套的，否则一片空白  #frame is a nightmare

		self.filepath_label=tk.Label(self.home_window)
		self.filepath_entry=tk.Entry(self.home_window)
		self.filepath_button=tk.Button(self.home_window)
		#self.source_folder_disp_label=tk.Label(self.home_window)
		#self.source_folder_disp=tk.Label(self.home_window)
		self.save_filepath_label=tk.Label(self.home_window)
		self.save_filepath_entry=tk.Entry(self.home_window)
		self.save_filepath_button=tk.Button(self.home_window)
		self.save_filename_entry=tk.Entry(self.home_window)
		self.save_filename_label=tk.Label(self.home_window)
		#self.save_folder_disp_label=tk.Label(self.home_window)
		#self.save_folder_disp=tk.Label(self.home_window)

		self.comp_method_label=tk.Label(self.home_window)
		self.comp_method_radio_button_string=tk.Radiobutton(self.home_window)
		self.comp_method_radio_button_properties=tk.Radiobutton(self.home_window)

		self.string_mode_label=tk.Label(self.home_window)
		self.string_mode_normal_label=tk.Label(self.home_window)
		self.string_mode_aggressive_label=tk.Label(self.home_window)
		self.string_mode_scale=tk.Scale(self.home_window)

		self.properties_mode_custom_weight_label=tk.Label(self.home_window)
		self.properties_mode_custom_weight_label_default_label=tk.Label(self.home_window)
		self.properties_mode_custom_weight_label_custom_checkbox=tk.Checkbutton(self.home_window)

		self.custom_weight_label_list=[]
		self.custom_weight_def_value_disp_list=[]
		self.custom_weight_entry_list=[]
		self.custom_weight_entry_var_list=[]

		self.start_button=tk.Button(self.home_window)

		self.__home_configuration()
		self.widgts=self.__init_custom_weight_elements()

	def __home_configuration(self):
		self.home_window.title(self.WINDOW_TITLE_NORMAL)
		self.home_window.geometry('640x400')
		self.home_window.resizable(False,False)
		#self.file_info_frame.place(x=300,y=0,anchor='n')

		self.filepath_label['text']='选择或输入源码文件夹'
		self.filepath_label['width']=self.label_width_long
		self.filepath_label.grid(column=0,columnspan=int(self.filepath_label['width']/self.column_single_width),row=0,padx=5)
		#self.filepath_label.place(x=10,y=10,anchor='w')
		self.filepath_entry['width']=self.entry_width_long
		self.filepath_entry['textvariable']=self.filepath_entry_variable
		self.filepath_entry.grid(column=int(self.filepath_label['width']/self.column_single_width),row=0,
						   columnspan=int(self.filepath_entry['width']/self.column_single_width),padx=5)
		#self.filepath_entry.place(x=40,y=10,anchor='center')
		self.filepath_button['text']='浏览'
		self.filepath_button['width']=self.button_width
		self.filepath_button['command']=lambda:self.__open_sys_filedialog(self.files_path,self.filepath_entry_variable)  
		#button的command直接写函数名，否则就会直接调用且无法作为command动作.使用lambda套壳以传递参数
		self.filepath_button.grid(column=int((self.filepath_label['width']+self.filepath_entry['width'])/self.column_single_width),row=0,
							columnspan=int(self.filepath_button['width']/self.column_single_width),padx=5)
		#self.filepath_button.place(x=90,y=10,anchor='e')
		#self.source_folder_disp_label['text']='当前源码文件夹'
		#self.source_folder_disp_label.grid(column=0,row=1,padx=5,pady=5)
		#self.source_folder_disp_label.place(x=0,y=0,anchor='w')
		#self.source_folder_disp['text']=self.files_path
		#self.source_folder_disp['textvariable']=self.filepath_entry_variable
		#self.source_folder_disp['justify']='left'
		#self.source_folder_disp.grid(column=1,row=1,columnspan=13,padx=5,pady=5)
		#self.source_folder_disp.place(x=10,y=0,anchor='e')

		self.save_filepath_label['text']='选择或输入存放\n结果文件的文件夹'
		self.save_filename_label['width']=self.label_width_long
		self.save_filepath_label.grid(column=0,row=3,
								columnspan=int(self.save_filename_label['width']/self.column_single_width),padx=5)
		self.save_filepath_entry['width']=self.entry_width_long
		self.save_filepath_entry['textvariable']=self.save_file_entry_variable
		self.save_filepath_entry.grid(column=int(self.save_filename_label['width']/self.column_single_width),row=3,
								columnspan=int(self.save_filepath_entry['width']/self.column_single_width),padx=5)
		self.save_filepath_button['text']='浏览'
		self.save_filepath_button['width']=self.button_width
		self.save_filepath_button['command']=lambda:self.__open_sys_filedialog(self.save_file_path,self.save_file_entry_variable)
		self.save_filepath_button.grid(column=int((self.save_filename_label['width']+self.save_filepath_entry['width'])/self.column_single_width),row=3,
								 columnspan=int(self.save_filepath_button['width']/self.column_single_width),padx=5)
		self.save_filename_label['text']='保存文件名'
		self.save_filename_label['width']=self.label_width_long
		self.save_filename_label.grid(column=0,row=4,
								columnspan=int(self.save_filename_label['width']/self.column_single_width),padx=5)
		self.save_filename_entry['width']=self.entry_width_long
		self.save_filename_entry['textvariable']=self.save_name_entry_variable
		self.save_filename_entry.grid(column=int(self.save_filename_label['width']/self.column_single_width),row=4,
								columnspan=int(self.save_filename_entry['width']/self.column_single_width),padx=5)
		#self.save_folder_disp_label['text']='当前结果保存文件夹'
		#self.save_folder_disp_label['width']=self.label_width
		#self.save_folder_disp_label.grid(column=0,row=4,padx=5,pady=5)
		#self.save_folder_disp['text']=self.save_file_path
		#self.save_folder_disp['textvariable']=self.save_file_entry_variable
		#self.save_folder_disp['justify']='left'
		#self.save_folder_disp['width']=self.entry_width8
		#self.save_folder_disp.grid(column=1,row=4,columnspan=13,padx=5,pady=5)

		self.comp_method_label['text']='选择比对算法'
		self.comp_method_label['width']=self.label_width_long
		self.comp_method_label.grid(column=0,row=5,
							  columnspan=int(self.comp_method_label['width']/self.column_single_width),padx=5)
		self.comp_method_radio_button_string['text']='字符串比对'
		self.comp_method_radio_button_string['width']=self.radio_width
		self.comp_method_radio_button_string['command']=self.__comp_method_string_command
		self.comp_method_radio_button_string['variable']=self.comp_method
		self.comp_method_radio_button_string['value']=self.COMP_METHOD_STRING
		self.comp_method_radio_button_string['state']='normal'
		self.comp_method_radio_button_string.grid(column=int(self.comp_method_label['width']/self.column_single_width)+3,row=5,
											columnspan=int(self.comp_method_radio_button_string['width']/self.column_single_width),padx=5)
		self.comp_method_radio_button_properties['text']='特征计数'
		self.comp_method_radio_button_properties['command']=self.__comp_method_properties_command
		self.comp_method_radio_button_properties['variable']=self.comp_method
		self.comp_method_radio_button_properties['value']=self.COMP_METHOD_PROPERTIES
		self.comp_method_radio_button_string['state']='normal'
		self.comp_method_radio_button_properties['width']=self.radio_width
		self.comp_method_radio_button_properties.grid(column=int((self.comp_method_label['width']+self.comp_method_radio_button_string['width'])/self.column_single_width)+5,row=5,
											columnspan=int(self.comp_method_radio_button_properties['width']/self.column_single_width),padx=5)
		
		#self.string_mode_scale['label']='运行模式'
		self.string_mode_label['text']='运行模式'
		self.string_mode_label['width']=self.label_width_long
		self.string_mode_normal_label['text']='函数内顺序对比'
		self.string_mode_normal_label['width']=int(self.label_width_long)
		self.string_mode_aggressive_label['text']='函数内行最大相似（更激进）'
		self.string_mode_aggressive_label['width']=self.label_width_long
		self.string_mode_scale['resolution']=1
		self.string_mode_scale['from']=1
		self.string_mode_scale['to']=2
		self.string_mode_scale['orient']='horizontal'
		self.string_mode_scale['length']=self.scale_width*self.scale_width_offset
		self.string_mode_scale['showvalue']=False

		self.properties_mode_custom_weight_label['text']='特征值'
		self.properties_mode_custom_weight_label['width']=self.label_width_long
		self.properties_mode_custom_weight_label_default_label['text']='默认权重'
		self.properties_mode_custom_weight_label_default_label['width']=self.label_width_short
		self.properties_mode_custom_weight_label_custom_checkbox['text']='自定义'
		self.properties_mode_custom_weight_label_custom_checkbox['width']=self.label_width_short
		self.properties_mode_custom_weight_label_custom_checkbox['variable']=self.custom_weight_check
		self.properties_mode_custom_weight_label_custom_checkbox['onvalue']=self.CHECK_BOX_ON
		self.properties_mode_custom_weight_label_custom_checkbox['offvalue']=self.CHECK_BOX_OFF
		self.properties_mode_custom_weight_label_custom_checkbox['command']=self.__checkbox_handle

		self.start_button['text']='开始'
		self.start_button['width']=self.button_width
		self.start_button['command']=self.__start_function
	
	def __open_sys_filedialog(self,path_variable,widgt_variable):
		path_variable=tk.filedialog.askdirectory()+'/'
		widgt_variable.set(path_variable)

	def __comp_method_string_command(self):
		self.__custom_weight_element_off()
		self.string_mode_label.grid(column=0,row=6,
							  columnspan=int(self.string_mode_label['width']/self.column_single_width),padx=0)
		self.string_mode_normal_label.grid(column=int(self.string_mode_label['width']/self.column_single_width),row=6,
									 columnspan=int(self.string_mode_label['width']/self.column_single_width),padx=0)
		self.string_mode_scale.grid(column=int((self.string_mode_label['width']+self.string_mode_normal_label['width'])/self.column_single_width),row=6,
							  columnspan=int(self.string_mode_scale['length']/8/self.column_single_width),padx=0)
		self.string_mode_aggressive_label.grid(column=int((self.string_mode_label['width']+self.string_mode_normal_label['width']+self.string_mode_scale['length']/self.scale_width_offset)/self.column_single_width),row=6,
										 columnspan=int(self.string_mode_aggressive_label['width']/self.column_single_width),padx=0)
		self.start_button.grid(column=9,row=7,columnspan=int(self.start_button['width']/self.column_single_width),padx=0)
		#self.start_button.pack(fill='x',anchor='s')

	def __comp_method_properties_command(self):
		self.__custom_weight_element_on()
		self.custom_weight_label_list=self.widgts['labels']
		self.custom_weight_def_value_disp_list=self.widgts['values']
		self.custom_weight_entry_list=self.widgts['entrys']
		self.custom_weight_entry_var_list=self.widgts['entry_vars']
		self.properties_mode_custom_weight_label.grid(column=0,row=6,
												columnspan=int(self.properties_mode_custom_weight_label['width']/self.column_single_width),padx=5)
		self.properties_mode_custom_weight_label_default_label.grid(column=int(self.properties_mode_custom_weight_label['width']/self.column_single_width)+self.def_weight_column_offset,row=6,
																columnspan=int(self.properties_mode_custom_weight_label_default_label['width']/self.column_single_width),padx=5)
		self.properties_mode_custom_weight_label_custom_checkbox.grid(column=int((self.properties_mode_custom_weight_label['width']+self.properties_mode_custom_weight_label_default_label['width'])/self.column_single_width)+6,row=6,
																columnspan=int(self.properties_mode_custom_weight_label_custom_checkbox['width']/self.column_single_width),padx=5)
		current_row=start_row=7
		for label in self.custom_weight_label_list:
			label.grid(column=0,row=current_row,
			  columnspan=int(self.label_width_long/self.column_single_width),padx=5)
			current_row+=1
		current_row=start_row
		for value in self.custom_weight_def_value_disp_list:
			value.grid(column=int(self.label_width_long/self.column_single_width)+self.def_weight_column_offset,row=current_row,
			  columnspan=int(self.label_width_short/self.column_single_width),padx=5)
			current_row+=1
		current_row=start_row
		for entry in self.custom_weight_entry_list:
			entry.grid(column=int((self.label_width_long+self.label_width_short)/self.column_single_width)+6,row=current_row,
			  columnspan=int(self.label_width_short/self.column_single_width),padx=5)
			current_row+=1
		self.__checkbox_handle()
		self.start_button.grid(column=9,row=current_row,columnspan=int(self.button_width/self.column_single_width),padx=5)

	def __custom_weight_element_on(self):
		self.string_mode_label.grid_forget()
		self.string_mode_normal_label.grid_forget()
		self.string_mode_scale.grid_forget()
		self.string_mode_aggressive_label.grid_forget()
		self.start_button.grid_forget()
		

	def __custom_weight_element_off(self):
		self.properties_mode_custom_weight_label.grid_forget()
		self.properties_mode_custom_weight_label_default_label.grid_forget()
		self.properties_mode_custom_weight_label_custom_checkbox.grid_forget()
		for label in self.custom_weight_label_list:
			label.grid_forget()
		for value in self.custom_weight_def_value_disp_list:
			value.grid_forget()
		for entry in self.custom_weight_entry_list:
			entry.grid_forget()
		self.start_button.grid_forget()

	def __init_custom_weight_elements(self):
		label_list=[]
		value_list=[]
		entry_list=[]
		entry_var_list=[]
		i=0
		for ele in def_weights:
			label_list.append(tk.Label(self.home_window,text=weights_name[ele]+':',width=self.properties_mode_custom_weight_label['width']))
			value_list.append(tk.Label(self.home_window,text=str(def_weights[ele]),width=self.properties_mode_custom_weight_label_default_label['width']))
			entry_var_list.append(tk.StringVar(self.home_window))
			entry_list.append(tk.Entry(self.home_window,width=self.properties_mode_custom_weight_label_custom_checkbox['width']))
			entry_list[i]['textvariable']=entry_var_list[i]
			i+=1
		return {'labels':label_list,'values':value_list,'entrys':entry_list,'entry_vars':entry_var_list}	

	def __custom_weight_entry_disable(self):
		current_row=7
		for entry in self.custom_weight_entry_list:
			#entry.grid_forget()
			entry['state']='disabled'
			#entry.grid(column=7,row=current_row)
			current_row+=1

	def __custom_weight_entry_enable(self):
		current_row=7
		for entry in self.custom_weight_entry_list:
			#entry.grid_forget()
			entry['state']='normal'
			#entry.grid(column=7,row=current_row)
			current_row+=1

	def __checkbox_handle(self):
		#self.custom_weight_check=self.properties_mode_custom_weight_label_custom_checkbox.getboolean()
		if self.custom_weight_check.get()==self.CHECK_BOX_OFF:
			self.__custom_weight_entry_disable()
		elif self.custom_weight_check.get()==self.CHECK_BOX_ON:
			self.__custom_weight_entry_enable()


	def __start_function(self):
		self.files_path=self.filepath_entry_variable.get()
		self.save_file_path=self.save_file_entry_variable.get()+'/'
		self.save_file_name=self.save_name_entry_variable.get()
		if len(self.files_path)==0:
			tk.messagebox.showwarning(title='文件夹路径为空',message='请选择源文件所在文件夹')
			return
		elif '/' not in self.files_path and '\\' not in self.files_path:
			if tk.messagebox.askyesno(title='文件夹路径异常',message='文件夹路径似乎不合法，要继续吗？')==False:
				return
		if len(self.save_file_path)==0:
			tk.messagebox.showwarning(title='文件夹路径为空',message='请选择要保存结果的文件夹')
			return
		elif '/' not in self.files_path and '\\' not in self.files_path:
			if tk.messagebox.askyesno(title='文件夹路径异常',message='文件夹路径似乎不合法，要继续吗？')==False:
				return
		if len(self.save_file_name)==0:
			tk.messagebox.showwarning(title='文件名为空',message='请输入结果文件的文件名')
			return
		for banned_symble in ['/','\\',':','*','?','"','<','>','|']:
			if banned_symble in self.save_file_name:
				tk.messagebox.showwarning(title='文件名错误',message='文件名中不能包含下列任何字符:\n \ / : * ? " < > |')
				return
		if self.comp_method.get()==self.COMP_METHOD_STRING:
			comp_method_ref=string_comparison
			if self.string_mode_scale.get()==1:
				method_string_mode=1
			elif self.string_mode_scale.get()==2:
				method_string_mode=2
			else:
				tk.messagebox.showerror(title='参数错误',message='运行模式参数错误')
				return
			custom_args=method_string_mode
		elif self.comp_method.get()==self.COMP_METHOD_PROPERTIES:
			comp_method_ref=properties_comp
			if self.custom_weight_check.get()==self.CHECK_BOX_ON:
				custom_weight_entry_value=[]
				custom_weights={}
				for entry_var in self.custom_weight_entry_var_list:
					if len(entry_var.get())==0:
						tk.messagebox.showwarning(title='自定义权重缺失',message='请补全自定义权重')
						return
					else:
						try:
							value=float(entry_var.get())
						except ValueError:
							tk.messagebox.showerror(title='自定义权重错误',message='权重值中有非法字符')
							return
						if value<0 or value>1:
							tk.messagebox.showerror(title='自定义权重错误',message='权重值超出0-1范围')
							return
					custom_weight_entry_value.append(value)
				if sum(custom_weight_entry_value)>1:
					tk.messagebox.showerror(title='自定义权重错误',message='权重之和大于1')
					return
				elif sum(custom_weight_entry_value)<1:
					tk.messagebox.showerror(title='自定义权重错误',message='权重之和小于1')
					return
				i=0
				for ele in def_weights:
					custom_weights[ele]=custom_weight_entry_value[i]
					i+=1
				print(custom_weights)
				custom_args=custom_weights
			else:
				custom_args=def_weights
		else:
			tk.messagebox.showerror(title='参数错误',message='算法选择参数错误')
			return
		self.home_window.title(self.WINDOW_TITLE_RUNNING)
		result=self.controllerRef.comp(self.files_path,custom_args,comp_method_ref)
		res_status=result['status']
		self.home_window.title(self.WINDOW_TITLE_NORMAL)
		if res_status==True:
			save_result=self.controllerRef.output_to_csv_proxy(result['result'],result['file_list'],self.save_file_path+self.save_file_name+'.csv')
			if save_result==True:
				tk.messagebox.showinfo(title='保存完成',message='结果已保存至'+self.save_file_path+self.save_file_name+'.csv'+'\n你可以使用Excel打开此文件以便查看')
			elif save_result==error_definition['FILE_SAVE_ERROR']:
				try:
					tk.messagebox.showerror(title='保存失败',message=error_info[save_result])
				except:
					tk.messagebox.showerror(title='保存失败',message='未知错误')
		else:
			try:
				tk.messagebox.showerror(title='运行失败',message=error_info[res_status])
			except:
				tk.messagebox.showerror(title='运行失败',message='未知错误')

	def ui_start(self):
		self.home_window.mainloop()