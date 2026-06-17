import os
import tempfile
from datetime import datetime

from assessments.models import PatientAssessment
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views import generic
from dotenv import load_dotenv
from fpdf import FPDF
from openai import OpenAI
from patients.models import Patient

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Brand palette (R, G, B)
TEAL       = (0, 124, 145)
DARK_TEAL  = (0, 77, 97)
LIGHT_TEAL = (240, 249, 250)
MID_GRAY   = (107, 114, 128)
LIGHT_GRAY = (245, 247, 250)
DARK       = (31, 41, 55)
WHITE      = (255, 255, 255)
GREEN      = (22, 163, 74)

FONT_ROOT   = os.path.join(settings.BASE_DIR, "static", "FisioVis", "fonts")
FONT_ROBOTO = os.path.join(FONT_ROOT, "roboto")


def _font(name, subdir=False):
    base = FONT_ROBOTO if subdir else FONT_ROOT
    return os.path.join(base, name)


def sanitize(text):
    for old, new in {
        "“": '"', "”": '"', "‘": "'", "’": "'",
        "–": "-", "—": "-", "•": "-", "…": "...",
    }.items():
        text = text.replace(old, new)
    return text


class ReportPDF(FPDF):
    def __init__(self, patient):
        super().__init__()
        self.patient = patient
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(12, 12, 12)
        self.add_font("Regular", "", _font("Roboto-Regular.ttf", subdir=True), uni=True)
        self.add_font("Bold",    "", _font("Roboto-Bold.ttf"),                uni=True)
        self.add_font("Italic",  "", _font("Roboto-Italic.ttf"),              uni=True)
        self.add_font("Light",   "", _font("Roboto-Light.ttf",  subdir=True), uni=True)

    # ------------------------------------------------------------------ #
    # Automatic header / footer (skip on cover page)                      #
    # ------------------------------------------------------------------ #

    def header(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(*TEAL)
        self.rect(0, 0, 210, 11, "F")
        self.set_font("Bold", "", 8)
        self.set_text_color(*WHITE)
        self.set_xy(12, 1.5)
        self.cell(90, 8, "FisioVis — Informe Clínico de Progreso Goniométrico")
        self.set_xy(108, 1.5)
        self.cell(90, 8, sanitize(self.patient.full_name), align="R")
        self.set_text_color(*DARK)
        self.set_y(14)

    def footer(self):
        y = self.h - 12
        self.set_fill_color(*TEAL)
        self.rect(0, y, 210, 12, "F")
        self.set_font("Italic", "", 8)
        self.set_text_color(*WHITE)
        self.set_y(-12)
        self.cell(0, 12,
                  f"Generado el {datetime.now().strftime('%d/%m/%Y')}  |  "
                  f"Página {self.page_no()}  |  FisioVis",
                  align="C")

    # ------------------------------------------------------------------ #
    # Section helpers                                                      #
    # ------------------------------------------------------------------ #

    def section_title(self, text):
        self.ln(3)
        self.set_font("Bold", "", 12)
        self.set_text_color(*TEAL)
        self.cell(0, 9, text, ln=True)
        y = self.get_y()
        self.set_fill_color(*TEAL)
        self.rect(12, y, 186, 0.4, "F")
        self.ln(4)
        self.set_text_color(*DARK)

    def sub_title(self, text):
        self.ln(2)
        self.set_font("Bold", "", 10)
        self.set_text_color(*DARK_TEAL)
        self.cell(0, 7, text, ln=True)
        self.set_text_color(*DARK)

    def body_text(self, text, line_height=6.5):
        self.set_font("Regular", "", 10)
        self.set_text_color(*DARK)
        self.multi_cell(0, line_height, sanitize(text))

    # ------------------------------------------------------------------ #
    # Cover page                                                           #
    # ------------------------------------------------------------------ #

    def cover_page(self, date_range, total_sessions):
        self.add_page()

        # Top teal band
        self.set_fill_color(*TEAL)
        self.rect(0, 0, 210, 52, "F")

        self.set_text_color(*WHITE)
        self.set_font("Bold", "", 38)
        self.set_y(10)
        self.cell(0, 16, "FisioVis", align="C", ln=True)

        self.set_font("Light", "", 12)
        self.cell(0, 7, "Sistema de Análisis y Seguimiento Fisioterapéutico", align="C", ln=True)

        # Body area
        self.set_text_color(*MID_GRAY)
        self.set_font("Light", "", 11)
        self.ln(30)
        self.cell(0, 8, "INFORME CLÍNICO DE PROGRESO GONIOMÉTRICO", align="C", ln=True)

        # Teal accent line
        self.ln(4)
        self.set_fill_color(*TEAL)
        self.rect(60, self.get_y(), 90, 0.8, "F")
        self.ln(7)

        # Patient name
        self.set_font("Bold", "", 22)
        self.set_text_color(*DARK)
        self.cell(0, 12, sanitize(self.patient.full_name), align="C", ln=True)

        self.set_font("Regular", "", 11)
        self.set_text_color(*MID_GRAY)
        self.cell(0, 7,
                  f"{self.patient.age} años  ·  {self.patient.get_sex_display()}",
                  align="C", ln=True)

        # Info pills
        self.ln(12)
        self.set_font("Regular", "", 10)
        self.set_text_color(*MID_GRAY)
        self.cell(0, 6, f"Período de evaluación:   {date_range}", align="C", ln=True)
        self.ln(2)
        self.cell(0, 6, f"Total de sesiones:   {total_sessions}", align="C", ln=True)
        self.ln(2)
        self.cell(0, 6,
                  f"Fecha de generación:   {datetime.now().strftime('%d de %B de %Y')}",
                  align="C", ln=True)

    # ------------------------------------------------------------------ #
    # Patient demographics                                                  #
    # ------------------------------------------------------------------ #

    def patient_section(self):
        self.section_title("Información del Paciente")

        rows = [
            ("Nombre completo",      sanitize(self.patient.full_name)),
            ("Edad",                 f"{self.patient.age} años"),
            ("Sexo",                 self.patient.get_sex_display()),
            ("Teléfono",             self.patient.phone or "—"),
            ("Correo electrónico",   self.patient.email or "—"),
            ("Trabajo / Ocupación",  sanitize(self.patient.work or "—")),
        ]

        for i, (label, value) in enumerate(rows):
            bg = LIGHT_GRAY if i % 2 == 0 else WHITE
            self.set_fill_color(*bg)
            self.set_font("Bold", "", 9.5)
            self.set_text_color(*MID_GRAY)
            self.cell(52, 7.5, label, fill=True)
            self.set_font("Regular", "", 9.5)
            self.set_text_color(*DARK)
            self.cell(134, 7.5, value, fill=True, ln=True)

        if self.patient.medical_history:
            self.ln(3)
            self.sub_title("Antecedentes médicos")
            self.body_text(self.patient.medical_history)

    # ------------------------------------------------------------------ #
    # Assessments table + progress summary                                #
    # ------------------------------------------------------------------ #

    def assessments_table(self, assessments):
        self.section_title("Historial de Evaluaciones Goniométricas")

        # Compute first angle per assessment type for delta column
        first_by_type = {}
        for a in assessments:
            first_by_type.setdefault(a.assessment.name, a.angle)

        # Header row
        col = [10, 32, 68, 28, 48]   # sum = 186
        self.set_fill_color(*DARK_TEAL)
        self.set_text_color(*WHITE)
        self.set_font("Bold", "", 9.5)
        for header, w in zip(["#", "Fecha", "Evaluación", "Ángulo", "Progreso"], col):
            self.cell(w, 8, header, fill=True, align="C")
        self.ln()

        # Data rows
        for i, a in enumerate(assessments):
            bg = LIGHT_TEAL if i % 2 == 0 else WHITE
            self.set_fill_color(*bg)
            self.set_font("Regular", "", 9.5)
            self.set_text_color(*DARK)

            first = first_by_type[a.assessment.name]
            delta = a.angle - first
            progress_text = (f"+{delta}°" if delta > 0 else f"{delta}°" if delta < 0 else "—")
            progress_color = GREEN if delta > 0 else MID_GRAY

            self.cell(col[0], 7.5, str(i + 1),                               fill=True, align="C")
            self.cell(col[1], 7.5, a.created_at.strftime("%d/%m/%Y"),         fill=True, align="C")
            self.cell(col[2], 7.5, a.assessment.name,                          fill=True)
            self.cell(col[3], 7.5, f"{a.angle}°",                             fill=True, align="C")

            self.set_font("Bold", "", 9.5)
            self.set_text_color(*progress_color)
            self.cell(col[4], 7.5, progress_text if i > 0 else "Inicio",      fill=True, align="C")
            self.set_text_color(*DARK)
            self.ln()

        self.ln(5)

        # --- Progress summary per assessment type ---
        self.sub_title("Resumen de mejora por evaluación")

        by_type = {}
        for a in assessments:
            by_type.setdefault(a.assessment.name, []).append(a)

        col2 = [68, 32, 32, 54]   # sum = 186
        self.set_fill_color(*DARK_TEAL)
        self.set_text_color(*WHITE)
        self.set_font("Bold", "", 9.5)
        for header, w in zip(["Evaluación", "Inicial", "Final", "Mejora total"], col2):
            self.cell(w, 8, header, fill=True, align="C")
        self.ln()

        for i, (name, records) in enumerate(by_type.items()):
            first = records[0].angle
            last  = records[-1].angle
            delta = last - first
            pct   = (delta / first * 100) if first else 0
            bg = LIGHT_TEAL if i % 2 == 0 else WHITE

            self.set_fill_color(*bg)
            self.set_font("Regular", "", 9.5)
            self.set_text_color(*DARK)
            self.cell(col2[0], 7.5, name,          fill=True)
            self.cell(col2[1], 7.5, f"{first}°",   fill=True, align="C")
            self.cell(col2[2], 7.5, f"{last}°",    fill=True, align="C")
            self.set_font("Bold", "", 9.5)
            self.set_text_color(*GREEN)
            self.cell(col2[3], 7.5, f"+{delta}° ({pct:.0f}%)", fill=True, align="C")
            self.set_text_color(*DARK)
            self.ln()

    # ------------------------------------------------------------------ #
    # AI analysis                                                          #
    # ------------------------------------------------------------------ #

    def analysis_section(self, text):
        self.add_page()
        self.section_title("Análisis Clínico — Generado por IA")

        lines = sanitize(text).split("\n")
        for line in lines:
            stripped = line.strip()
            if not stripped:
                self.ln(2)
                continue

            # Detect numbered section headers: "1. TITLE" or "1. Title"
            is_num_header = (
                len(stripped) > 2 and
                stripped[0].isdigit() and
                stripped[1] in ".)" and
                len(stripped) < 90
            )
            if is_num_header:
                clean = stripped[2:].strip().lstrip(". ")
                self.ln(3)
                self.set_font("Bold", "", 11)
                self.set_text_color(*TEAL)
                self.multi_cell(0, 7, clean)
                self.set_fill_color(*TEAL)
                y = self.get_y()
                self.rect(12, y, 186, 0.3, "F")
                self.ln(3)
                self.set_text_color(*DARK)
            else:
                self.body_text(stripped)
                self.ln(1)


# ------------------------------------------------------------------ #
# Views                                                               #
# ------------------------------------------------------------------ #

class PatientListView(LoginRequiredMixin, generic.ListView):
    model = Patient
    template_name = "reports/patients.html"
    context_object_name = "patient"

    def get_queryset(self):
        return Patient.objects.filter(is_active=True, user=self.request.user)


def create_report(request, id):
    patient = get_object_or_404(Patient, id=id)
    raw = get_list_or_404(PatientAssessment, patient=patient, is_active=True)
    assessments = sorted(raw, key=lambda a: a.created_at)

    dates      = [a.created_at for a in assessments]
    date_range = f"{min(dates).strftime('%d/%m/%Y')} – {max(dates).strftime('%d/%m/%Y')}"

    data_lines = [
        f"  - {a.created_at.strftime('%d/%m/%Y')}: {a.assessment.name} → {a.angle}°"
        for a in assessments
    ]

    prompt = (
        f"Eres un fisioterapeuta clínico experto. Redacta un informe profesional y técnico.\n\n"
        f"PACIENTE:\n"
        f"- Nombre: {patient.full_name}\n"
        f"- Edad: {patient.age} años | Sexo: {patient.get_sex_display()}\n"
        f"- Antecedentes: {patient.medical_history or 'Sin antecedentes registrados'}\n"
        f"- Trabajo: {patient.work or 'No especificado'}\n\n"
        f"EVALUACIONES GONIOMÉTRICAS (orden cronológico):\n"
        + "\n".join(data_lines) +
        "\n\nEscribe el informe con EXACTAMENTE estas 5 secciones numeradas "
        "(sin markdown, sin asteriscos, lenguaje clínico formal, 2-3 párrafos cada una):\n\n"
        "1. RESUMEN EJECUTIVO\n"
        "2. ANÁLISIS DE EVOLUCIÓN\n"
        "3. COMPARACIÓN CON RANGOS NORMALES\n"
        "4. CONCLUSIONES CLÍNICAS\n"
        "5. RECOMENDACIONES\n"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1400,
        temperature=0.35,
    )
    analysis = response.choices[0].message.content

    # Build PDF
    pdf = ReportPDF(patient)
    pdf.cover_page(date_range, len(assessments))

    pdf.add_page()
    pdf.patient_section()
    pdf.ln(4)
    pdf.assessments_table(assessments)

    pdf.analysis_section(analysis)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in patient.full_name)
        file_resp = FileResponse(
            open(tmp.name, "rb"),
            as_attachment=True,
            filename=f"informe_{safe_name}.pdf",
            content_type="application/pdf",
        )
        file_resp.set_cookie("report_ready", "1", max_age=30)
        return file_resp
