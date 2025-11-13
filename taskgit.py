from abc import ABC, abstractmethod
from datetime import datetime
from reportlab.pdfgen import canvas 
from reportlab.lib.pagesizes import letter
import openpyxl

class InvoiceGenerator(ABC):

    def __init__(self, client_name, iteems):
        self.client_name = client_name
        self.items = iteems
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def calculate_total(self):
        return sum(item['price'] for item in self.items)
    
    @abstractmethod
    def generate_invoice(self):
        pass

class PDFInvoiceGenerator(InvoiceGenerator):

    def generate_invoice(self):
        fileneme =  f"invoce_{self.client_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        pdf = canvas.Canvas(fileneme, pagesize=letter)

        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(100, 750, "INVOICE")

        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 720, f"Client: {self.client_name}")
        pdf.drawString(100, 700, f"Date: {self.date}")

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(100,670,"items:")

        pdf.setFont("Helvetica",11)
        y_position = 650
        for item in self.items:
            pdf.drawString(120, y_position, f"-{item['name']}: ${item['price']}")
            y_position -= 20
        

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(100,y_position - 20, f"Total:${self.calculate_total()}")

        pdf.save()
        return fileneme
    
class ExelInvoiceGenerator(InvoiceGenerator):

    def generate_invoice(self):
        filename = f"invoice_{self.client_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx"
       
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Invoice"

        ws['A1'] = "INVOICE"
        ws['A1'].font = openpyxl.styles.Font(size=16, bold=True)
        ws['A3'] = f"Client: {self.client_name}"
        ws['A4'] = f"Date: {self.date}"


        ws['A6'] = "Product Name"
        ws['B6'] = "Price"
        ws['A6'].font = openpyxl.styles.Font(bold=True)
        ws['B6'].font = openpyxl.styles.Font(bold=True)

        row = 7
        for item in self.items:
            ws[f'A{row}'] = item['name']
            ws[f'B{row}'] = item['price']
            row += 1


        ws[f'A{row}'] = "TOTAL"

print('Something...')