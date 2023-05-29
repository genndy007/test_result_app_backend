from fpdf import FPDF


class TestRunReportPDF:
    def __init__(self, file_name):
        self.file_name = file_name
        self.pdf = FPDF()

    def prepare(self):
        self.pdf.set_font("helvetica", "B", 16)

    def build_pdf(self):
        self.pdf.cell(40, 10, "Hello World!")

    def make(self):
        self.prepare()
        self.pdf.add_page()
        self.build_pdf()
        self.pdf.output(self.file_name)
