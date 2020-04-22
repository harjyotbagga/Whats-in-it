from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import UploadImageForm, UploadURLForm
from django.conf.urls.static import static
from clarifai.rest import ClarifaiApp
from decouple import config
import json
import base64
import os

app = ClarifaiApp(api_key=config('API_KEY'))
model = app.models.get(model_id=config('MODEL_ID'))

def home(request):
    image_form = UploadImageForm()
    url_form = UploadURLForm()
    context = {'image_form': image_form, 'url_form': url_form}
    
    if request.method == 'POST':
        
        if request.POST.get('submit') == 'Search via URL':
            url = request.POST.get('url_field')
            response = model.predict_by_url(url=url)
            context['source_img'] = url
        
        elif request.POST.get('submit') == 'Search via Image':
            image = request.FILES['image_field']
            fs = FileSystemStorage()
            image_name = 'image.jpg'
            fs.delete(image_name)
            fs.save(image_name, image)
            image_loc = os.path.join(settings.MEDIA_ROOT, image_name)
            response = model.predict_by_filename(image_loc)
            context['source_img'] = '/media/image.jpg'
        
        response_object = response['outputs'][0]['data']['concepts']
        ingredients = []
        for i in response_object:
            i_detail = [i['name'], i['value']]
            ingredients.append(i_detail)
        context['ingredients'] = ingredients
    return render(request, 'index.html', context=context)