import base64
from io import BytesIO
from django.utils.encoding import force_str
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from PIL import Image
from tensorflow import keras

from authentication.predictions import make_predictions

model = keras.models.load_model(
    'C:/Users/Ala/Documents/dog vs cat/model/model/model')


def home(request):
    if request.method == "POST":
        image = request.FILES['uploaded-file']
        predicted_class = make_predictions(image, model)
        class_name = "Pies" if predicted_class == "Dogs" else "Kot"
        pil_image = Image.open(image)

        buffered = BytesIO()
        pil_image.save(buffered, format="JPEG")
        image_as_string = "data:image/jpeg;base64," + force_str(base64.b64encode(buffered.getvalue()))

        return render(request, "authentication/index.html",
                      {"predicted_class": class_name,
                       "image_as_string": image_as_string})
    else:
        return render(request, "authentication/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')

        User.objects.create_user(username=username, password=password1)

        return redirect("signin")
    else:
        return render(request, "authentication/signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']

        user = authenticate(username=username, password=password1)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Niepoprawne dane logowania")
            return render(request, "authentication/index.html")

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    return redirect("home")
