from fpdf import FPDF

from src.core.pdf.common import FONT_FAMILY, Font, Color
from src.core.pdf.mapping import STATUS_MAPPING


class ReportPDF:
    def __init__(self, file_name, data):
        self.file_name = file_name
        self.data = data
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

    def build_report_heading(self):
        self.pdf.set_font(*Font.REPORT_HEADING)
        self.pdf.set_fill_color(*Color.WHITE)
        self.pdf.cell(self.pdf.epw, Font.HEADING_FONT_SIZE, 'Test Run Report', align='C', fill=True)
        self.pdf.ln()
        self.pdf.ln(5)

    def build_title(self):
        self.pdf.set_font(*Font.GENERAL_HEADING)
        self.pdf.set_fill_color(*Color.WHITE)

        row1 = {
            'Test Suite': self.data['test_suite']['name'],
            'Date': self.data['timestamp'],
        }
        row2 = {
            'About suite': self.data['test_suite']['description'],
            'Result of Run': STATUS_MAPPING.get(self.data['result'], 'UNKNOWN'),
        }
        rows = [row1, row2]

        for row in rows:
            for key, value in row.items():
                self.pdf.set_font(*Font.GENERAL_HEADING)
                self.pdf.set_fill_color(*Color.HEADING)
                self.pdf.cell(self.pdf.epw * 0.2, Font.GENERAL_FONT_SIZE, key, align='L', fill=True)

                self.pdf.set_font(*Font.GENERAL_TEXT)
                self.pdf.set_fill_color(*Color.WHITE)
                self.pdf.cell(self.pdf.epw * 0.3, Font.GENERAL_FONT_SIZE, value, align='L', fill=True)

            self.pdf.ln()

        self.pdf.ln(5)

    def build_test_cases_heading(self):
        self.pdf.set_font(*Font.GENERAL_HEADING)
        self.pdf.set_fill_color(*Color.WHITE)
        self.pdf.cell(self.pdf.epw, Font.HEADING_FONT_SIZE, 'Test Cases List', align='C', fill=True)
        self.pdf.ln()

    def build_one_test_case(self, test_case):
        pass

    def build_pdf(self):
        self.build_report_heading()
        self.build_title()
        self.build_test_cases_heading()
