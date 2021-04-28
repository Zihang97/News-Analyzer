import PyPDF2 as pypdf

def extract_data(fileaddr):
	pdfobject = open(fileaddr,'rb')
	pdf = pypdf.PdfFileReader(pdfobject)

	info_dict = {}
	temp = pdf.getDocumentInfo()
	info_dict['author'] = temp['/Creator'][0:5]
	info_dict['create_time'] = temp['/CreationDate']
	info_dict['modified_time'] = temp['/ModDate']
	
	# content = ''
	# for i in range(pdf.numPages):
	# 	page = pdf.getPage(i)
	# 	content += page.extractText()

	# info_dict['content'] = content

	pdfobject.close()

	return info_dict

# print(extract_data('./File_buffer/VQA_Project1_Report.pdf'))

# def findInDict(needle, haystack):
#     for key in haystack.keys():
#         try:
#             value=haystack[key]
#         except:
#             continue
#         if key==needle:
#             return value
#         if isinstance(value,dict):            
#             x=findInDict(needle,value)            
#             if x is not None:
#                 return x
# xfa=findInDict('/XFA',pdf.resolvedObjects)
# xml=xfa[7].getObject().getData()