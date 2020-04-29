from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal


def parse(file_path, lines_to_return=None, pages=None):
    if not lines_to_return and not pages:
        raise ValueError('Either lines_to_return or pages count must be provided')

    with open(file_path, 'rb') as file_stream:
        lines = []
        resource_manager = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(resource_manager, laparams=laparams)
        interpreter = PDFPageInterpreter(resource_manager, device)
        for index, page in enumerate(PDFPage.get_pages(file_stream)):
            if pages and index >= pages:
                break

            interpreter.process_page(page)
            layout = device.get_result()
            for element in layout:
                if isinstance(element, LTTextBoxHorizontal):
                    lines.extend(element.get_text().splitlines())

                    if lines_to_return and len(lines) >= lines_to_return:
                        break

        return lines
