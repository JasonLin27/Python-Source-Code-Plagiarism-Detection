import keyword

def key_codes_initial():  #初始化关键字码的字典
	codes_dict={}
	no=100
	for kw in keyword.kwlist:
		codes_dict[kw]=no
		no+=1
	return codes_dict

def sim_codes_initial():  #初始化符号码的字典
	sym_dict={}
	no=400
	symlist=['+','-','*','/','%','//',
		  '<','>','<=','>=','<>','!=',
		  '(',')','[',']','{','}',
		  ':',',','\\','"',"'",'"""',"'''",'#',
		  '.','@',
		  '!','&','|','~','^','<<','>>',
		  '**=','//=','**','+=','-=','*=','/=','%=',
		  '=','==',]
	for sym in symlist:
		sym_dict[sym]=no
		no+=1
	return sym_dict

#潜在的编码问题：限制了变量和常量为最大99个，否则产生编码混淆

#关键字
KEY_CODE=key_codes_initial()

#常量（数字、字符串）
CONST_CODE=200

#变量
VAR_CODE=300

#符号
SYM_CODE=sim_codes_initial()

#错误
ERROR_CODE=500

#注释
ANO_CODE=600
#常量、变量和注释编码和关键字、符号不同，为从X01开始

#编码后附带的字母，标识词的类型，用于解决潜在的编码问题
TYPE_CODE={'key':'K','const':'C','var':'V','sym':'S','ano':'A','err':'E'}

#数字识别相关
bindigit=['0','1']
octdigit=bindigit+['2','3','4','5','6','7']
digit=octdigit+['8','9']
nonzerodigit=['1','2','3','4','5','6','7','8','9']
hexdigit=['a','b','c','d','e','f','A','B','C','D','E','F']+digit

#字符串比对中切分各部分的权重
str_comp_weights={
	'import':0.1,
	'func':0.8,
	'other':0.1,
	}

#属性计数中默认特征权重(百分比小数）
def_weights={
'var':0.15,
'const':0.15,
'func':0.04,
'judge':0.15,
'loop':0.15,
'error':0.12,
'arith_op':0.12,
'value_assign':0.12,
}

weights_name={
'var':'变量数量',
'const':'常量数量',
'func':'函数数量',
'judge':'判断分支数量',
'loop':'循环结构数量',
'error':'错误处理数量',
'arith_op':'运算操作数量',
'value_assign':'赋值操作数量',
}

#错误类型定义
error_definition={
	'NO_SOURCE_FILES_ERROR':701,
	'SOURCE_FILE_NOT_ENOUGH_ERROR':702,
	'CUSTOM_ARGS_ERROR':703,
	'FILE_SAVE_ERROR':704,
	'INVALID_FUNCTION_NAME':705,
	'INVALID_FILE_TYPE':706,
	'FILE_ACCESS_FAILED':707,
	'LEXICAL_ANALYSIS_INVALID_CHAR':708,
	'LEXICAL_ANALYSIS_COMPLEX_FORMAT_ERROR':709,
	'LEXICAL_ANALYSIS_FLOAT_FORMAT_ERROR':710,
	'LEXICAL_ANALYSIS_INVALID_FUNCTION_ARGS':711,
	'LEXICAL_ANALYSIS_INVALID_PAIR_STATUS':712,
	'LEXICAL_ANALYSIS_INCONSISTENT_TAB':713,
	'LEXICAL_ANALYSIS_QUOTE_NOT_IN_PAIR':714,
	'LEXICAL_ANALYSIS_INVALID_VARIABLE_NAME':715,
	}

error_info={
	701:'未找到源代码文件',
	702:'源代码文件不足',
	703:'自定义参数错误',
	704:'写文件出现错误，文件被占用或只读',
	705:'调用的函数名称不合法',
	706:'不是python源代码文件',
	707:'文件访问失败',
	708:'词法分析失败:非法字符',
	709:'词法分析失败：复数格式错误',
	710:'词法分析失败：浮点数格式错误',
	711:'词法分析失败：函数参数错误',
	712:'词法分析失败：引号配对状态错误',
	713:'词法分析失败：缩进空格未对齐(4空格为1缩进)',
	714:'词法分析失败：引号未配对',
	715:'词法分析失败：非法变量名',
	}