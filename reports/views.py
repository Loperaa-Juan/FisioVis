import os
import tempfile
from datetime import datetime

from assessments.models import Patient, PatientAssessment
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views import generic
from dotenv import load_dotenv
from fpdf import FPDF
from openai import OpenAI

# import unicodedata


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def sanitize_text(text):
    replacements = {
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "–": "-",
        "—": "-",
        "•": "-",
        "…": "...",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.ln(1)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(
            0, 10, f"Generado el {datetime.now().strftime('%d/%m/%Y')}", align="C"
        )


# Create your views here.
class PatientListView(LoginRequiredMixin, generic.ListView):
    model = Patient
    template_name = "reports/patients.html"
    context_object_name = "patient"

    def get_queryset(self, queryset=None):
        return Patient.objects.filter(is_active=True, user=self.request.user)


def create_report(request, id):
    patient = get_object_or_404(Patient, id=id)
    assessments = get_list_or_404(PatientAssessment, patient=patient)

    data = "\n".join(
        [
            f"- {a.created_at.strftime('%Y-%m-%d')}: {a.assessment} → {a.angle}°"
            for a in assessments
        ]
    )

    prompt = f"""
    Genera un informe de progreso clínico centrado en goniometría.
    Usa los siguientes datos de evolución:

    {data}

    Redáctalo en párrafos técnicos, describiendo la evolución del rango de movimiento
    y la mejoría funcional observada entre las fechas. Mantén un tono formal y profesional.
    """

    response = client.responses.create(model="gpt-5", input=prompt)

    informe = sanitize_text(response.output_text)

    Black = os.path.join(
        settings.BASE_DIR, "static", "FisioVis", "fonts", "Roboto-Black.ttf"
    )

    Bold = os.path.join(
        settings.BASE_DIR, "static", "FisioVis", "fonts", "Roboto-Bold.ttf"
    )

    Italic = os.path.join(
        settings.BASE_DIR, "static", "FisioVis", "fonts", "Roboto-Italic.ttf"
    )
    # Generar PDF
    pdf = PDF()

    # --- Espaciado y cuerpo ---
    pdf.add_page()
    pdf.add_font("RobotoBlack", "", Black, uni=True)
    pdf.add_font("RobotoBold", "", Bold, uni=True)
    pdf.add_font("RobotoItalic", "", Italic, uni=True)

    # --- Título ---
    pdf.set_font("RobotoBold", "", 32)
    pdf.set_text_color(0, 124, 145)
    
    pdf.cell(0, 15, "FisioVis", align="C", ln=True)

    # --- Subtítulo ---
    pdf.set_font("RobotoBlack", "", 16)
    pdf.set_text_color(0, 77, 97)

    pdf.cell(
        0,
        10,
        "Sistema de Análisis y Seguimiento Fisioterapéutico",
        align="C",
        ln=True,
    )

    # --- Espacio ---
    pdf.ln(30)  

    # --- Encabezado del informe ---
    pdf.set_text_color(0, 0, 0)

    pdf.multi_cell(0, 8, "Informe de Progreso Goniométrico\n", align="C")

    # --- Paciente ---

    pdf.multi_cell(0, 8, f"Paciente: {patient.full_name}", align="C")

    # --- Espacio ---
    pdf.ln(5)

    # --- Resto del documento ---
    pdf.set_font("RobotoItalic", "", 12)
    pdf.set_text_color(128, 128, 128)

    pdf.add_page()
    pdf.set_font("RobotoBlack", "", 12)
    clean_text = informe.replace("“", '"').replace("”", '"')
    clean_text = clean_text.replace("‘", "'").replace("’", "'")
    pdf.multi_cell(0, 10, clean_text, align="J")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        return FileResponse(
            open(tmp_file.name, "rb"),
            as_attachment=True,
            filename="informe_goniometria.pdf",
        )
