from django import forms

from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "full_name",
            "age",
            "sex",
            "phone",
            "email",
            "work",
            "medical_history",
            "surgeries",
            "pathologies",
            "medications",
            "photo",
        ]
        widgets = {
            "full_name": forms.TextInput(),
            "work": forms.TextInput(),
            "photo": forms.FileInput(attrs={"accept": "image/*", "class": "hidden", "id": "photo-input"}),
            "medical_history": forms.Textarea(attrs={"rows": 3}),
            "surgeries": forms.Textarea(attrs={"rows": 2}),
            "pathologies": forms.Textarea(attrs={"rows": 2}),
            "medications": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        placeholders = {
            "full_name": "Juan García López",
            "age": "35",
            "phone": "+57 300 000 0000",
            "email": "correo@ejemplo.com",
            "work": "Fisioterapeuta, oficinista, estudiante…",
            "medical_history": "Describa antecedentes médicos relevantes…",
            "surgeries": "Ninguna / descripción de cirugías…",
            "pathologies": "Ninguna / descripción de patologías…",
            "medications": "Ninguna / medicamentos actuales…",
        }
        for name, field in self.fields.items():
            if name == "photo":
                continue
            attrs = {"class": "border border-gray-300 w-full rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500"}
            if name in placeholders:
                attrs["placeholder"] = placeholders[name]
            field.widget.attrs.update(attrs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
