from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


def parse(pdf_path):

    fp = open(pdf_path, 'rb')

    parser = PDFParser(fp)

    doc = PDFDocument()

    parser.set_document(doc)
    doc.set_parser(parser)

    doc.initialize()

    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        rsrcmgr = PDFResourceManager()

        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        interpreter = PDFPageInterpreter(rsrcmgr, device)

        out = ''
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()

            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    results = x.get_text()
                    out += results
        return out



if __name__ == '__main__':
    pdf_path = './File_buffer/Machine.pdf'
    print(parse(pdf_path))
    