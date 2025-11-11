import base64
import json

import cv2
import mediapipe as mp
import numpy as np
import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from patients.models import Patient

from .models import Assessment, PatientAssessment

ESP32_URL = "http://192.168.1.9/capture"


def calculate_angle(a, b, c):
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
        a[1] - b[1], a[0] - b[0]
    )
    angle = np.abs(radians * 180.0 / np.pi)
    # if angle > 180.0:
    #     angle = 360 - angle
    return angle


def evaluate(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido")

    try:
        body_str = request.body.decode("utf-8")
        if not body_str:
            return JsonResponse({"error": "Body vacío"}, status=400)

        data = json.loads(body_str)
        exam_type = data.get("exam_type")

        if not exam_type:
            return JsonResponse(
                {"error": "Falta 'exam_type' en el JSON body"}, status=400
            )

        esp_response = requests.get(ESP32_URL, timeout=10)
        if esp_response.status_code != 200:
            return JsonResponse(
                {"error": "No se pudo obtener la imagen del ESP32"}, status=500
            )

        img_bytes = esp_response.content
        np_img = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        resized = cv2.resize(frame, (224, 224))

        mp_pose = mp.solutions.pose
        with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
            results = pose.process(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                angle = 0
                points_to_draw = []

                match exam_type:
                    case "ROM Hombro D":
                        p1 = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                        p2 = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                        p3 = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
                        angle = calculate_angle(p1, p2, p3)
                        points_to_draw = [p1, p2, p3]

                    case "ROM Hombro I":
                        p1 = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                        p2 = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                        p3 = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
                        angle = calculate_angle(p1, p2, p3)
                        points_to_draw = [p1, p2, p3]

                    case "ROM Codo D":
                        p1 = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                        p2 = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
                        p3 = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
                        angle = calculate_angle(p1, p2, p3)
                        points_to_draw = [p1, p2, p3]

                    case "ROM Codo I":
                        p1 = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                        p2 = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
                        p3 = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
                        angle = calculate_angle(p1, p2, p3)
                        points_to_draw = [p1, p2, p3]

                    case _:
                        return JsonResponse(
                            {"error": "Tipo de examen no reconocido"}, status=400
                        )

                h, w, _ = resized.shape

                pixel_points = [(int(p.x * w), int(p.y * h)) for p in points_to_draw]

                for point in pixel_points:
                    cv2.circle(resized, point, 5, (0, 255, 255), -1)

                cv2.line(resized, pixel_points[0], pixel_points[1], (255, 0, 0), 2)
                cv2.line(resized, pixel_points[1], pixel_points[2], (255, 0, 0), 2)

                cv2.putText(
                    resized,
                    f"{int(angle)}°",
                    (pixel_points[1][0] + 10, pixel_points[1][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )

                _, buffer = cv2.imencode(".jpg", resized)
                image_base64 = base64.b64encode(buffer).decode("utf-8")

                return JsonResponse({"image": image_base64, "angle": int(angle)})

            else:
                return JsonResponse(
                    {"error": "No se detectaron puntos corporales."}, status=422
                )

    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido en el body"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def assessment_view(request, id):
    patient = Patient.objects.get(id=id)
    assesments = Assessment.objects.get_queryset()
    return render(
        request,
        "assessments/assessment.html",
        {"patient": patient, "assessments": assesments},
    )


@csrf_exempt
def save_assessment(request):
    if request.method == "POST":
        patient_id = request.POST.get("patient_id")
        assessment_name = request.POST.get("assessment")
        angle = request.POST.get("angle")
        image = request.FILES.get("image")

        if not image:
            return JsonResponse({"error": "No se envió ninguna imagen"}, status=400)

        patient = get_object_or_404(Patient, id=patient_id)
        assesment = get_object_or_404(Assessment, name=assessment_name)

        assessment = PatientAssessment.objects.create(
            patient=patient, assessment=assesment, angle=angle, photo=image
        )
        return JsonResponse(
            {
                "message": "Imagen guardada correctamente",
                "image_url": assessment.photo.url,
            }
        )
