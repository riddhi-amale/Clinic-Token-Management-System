from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.image("website\static\website\logo.jpg")
        self.ln(10)
        self.set_font("helvetica","",16)
        self.set_x(10)
        self.set_fill_color(151,166,6)
        self.set_text_color(0,0,0)
        self.cell(self.w-20, 10, "  Dr Sandeep Shah", ln=1,align="L",fill=1)
        self.ln(5)
    
    def footer(self):
        self.set_font("helvetica","",12)
        self.set_x(10)
        self.set_y(-40)
        self.set_fill_color(151,166,6)
        self.set_text_color(0,0,0)
        self.cell(self.w-20, 8, "Phone number: +91 9890885210", ln=1,align="R",fill=1)
        self.cell(self.w-20, 8, "Address: Opp. Sonai Mangal Karyalaya, Pawar Nagar,Colony no. 3,Thergaon, Pune-33", ln=1,align="R",fill=1)
        self.ln(20)

def generate_pdf(name, phone_number, my_token, formatted_date,time):
    pdf = PDF('P','mm','letter')
    pdf.add_page()
    pdf.set_font("helvetica","",16)
    pdf.cell(40,10,'Name: '+name,ln=True)
    pdf.cell(40,10,'Phone Number: '+phone_number,ln=True)
    pdf.cell(40,10,'Date of appointment: '+formatted_date,ln=True)
    if time =="morning":
        pdf.cell(40,10,'Time Slot: 10:00am - 01:00pm',ln=True)
    else:
        pdf.cell(40,10,'Time Slot: 05:00pm - 08:00pm',ln=True)
    pdf.cell(40,10,'Token Number: '+my_token,ln=True)
    pdf.set_y(-55)
    pdf.cell(40,10,"If your token is missed your appointment will be cancelled!")
    pdf.output("my_appointment.pdf")