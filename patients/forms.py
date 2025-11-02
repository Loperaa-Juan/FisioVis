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
        ]
        widgets = {
            "medical_history": forms.Textarea(attrs={"rows": 3}),
            "surgeries": forms.Textarea(attrs={"rows": 2}),
            "pathologies": forms.Textarea(attrs={"rows": 2}),
            "medications": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # <--- recibiremos el user aquí
        super().__init__(*args, **kwargs)

        # Tailwind setup
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "border border-gray-300 w-full rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500"
                }
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
