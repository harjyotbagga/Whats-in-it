from clarifai.rest import ClarifaiApp
import json
from decouple import config

app = ClarifaiApp(api_key=config('API_KEY')

model = app.models.get(model_id=config('MODEL_ID'))
image_url = 'https://samples.clarifai.com/food.jpg'
response = model.predict_by_url(url=image_url)
#response = model.predict_by_filename('/home/user/image.jpeg')

response_object = response['outputs'][0]['data']['concepts']
ingredients = []
for i in response_object:
    i_detail = [i['name'], i['value']]
    ingredients.append(i_detail)
# response_object = json.loads(response)
# formatted_response = json.dumps(response_object, indent=2)
# print(formatted_response)

print(ingredients)

# f = open('output.txt', 'w')
# f.write(formatted_response)
# f.close()