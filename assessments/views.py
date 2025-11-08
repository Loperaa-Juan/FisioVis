import base64
import os

import cv2
import numpy as np
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
from dotenv import load_dotenv
from openai import OpenAI
from patients.models import Patient

from .models import Assessment

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ESP32_URL = "http://192.168.1.8/capture"


def evaluate(request):
    try:
        esp_response = requests.get(ESP32_URL, timeout=10)
        if esp_response.status_code != 200:
            return JsonResponse(
                {"error": "No se pudo obtener la imagen del ESP32"}, statu=500
            )

        img_bytes = esp_response.content

        np_img = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        resized = cv2.resize(frame, (224, 224))

        _, buffer = cv2.imencode(".jpg", resized)
        image_base64 = base64.b64encode(buffer).decode("utf-8")

        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente médico que analiza imágenes médicas capturadas por una cámara ESP32-CAM.",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analiza esta imagen y describe lo que observas, sé breve:",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                },
            ],
        )

        result = response.choices[0].message.content
        return JsonResponse({"image": image_base64, "analysis": result})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def assessment_list_view(request, id):
    patient = Patient.objects.get(id=id)
    assesments = Assessment.objects.get_queryset()
    return render(
        request,
        "assessments/list_assessments.html",
        {"patient": patient, "assessments": assesments},
    )


class AssessmentView(LoginRequiredMixin, generic.TemplateView):
    template_name = "assessments/assessment.html"
