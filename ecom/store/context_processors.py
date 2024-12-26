from .models import Category, ImageForLogo

def categories(request):
    return {'categories': Category.objects.all()}

def logo(request):
    return {'logo': ImageForLogo.objects.all().last()}
