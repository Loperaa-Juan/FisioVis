from django.views.generic import TemplateView


class LandingView(TemplateView):
    template_name = "landing.html"

class AboutView(TemplateView):
    template_name = 'about.html'