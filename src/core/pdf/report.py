from fpdf import FPDF

from src.core.pdf.common import FONT_FAMILY, Font, Color


class ReportPDF:
    def __init__(self, file_name):
        self.file_name = file_name
        self.pdf = FPDF()

    def prepare(self):
        self.pdf.set_line_width(1 / 10 ** 5)

    def build_pdf(self):
        pass

    def make(self):
        self.prepare()
        self.pdf.add_page()
        self.build_pdf()
        self.pdf.output(self.file_name)


class TestRunReportPDF(ReportPDF):
    def build_heading(self):
        self.pdf.set_font(*Font.REPORT_HEADING)
        self.pdf.set_fill_color(*Color.WHITE)
        self.pdf.cell(self.pdf.epw, Font.HEADING_FONT_SIZE, 'Test Run Report', align='C', fill=True)
        self.pdf.ln()

    def build_pdf(self):
        self.build_heading()
