import requests
import uuid
import json
import settings


class AzureTranslate():
    PATH = '/translate?api-version=3.0'
    def __init__(self):
        self.subcription_key = settings.TRANSLATOR_TEXT_SUBSCRIPTION_KEY
        self.endpoint = settings.TRANSLATOR_TEXT_ENDPOINTS

    def translate_to_english(self, text_to_translate:str):
        """ translate text to english """
        return self.translate(text_to_translate, 'en')
        

    def translate(self, text_to_translate:str, target_language:str='de'):
        """ detect and translate text """
        #define header
        headers = {
            'Ocp-Apim-Subscription-Key': self.subcription_key,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
        params = '&to={}'.format(target_language)
        constructed_url = self.endpoint + self.PATH + params


        body = [{
            'text': text_to_translate
        }]

        request = requests.post(constructed_url, headers=headers, json=body)
        response = request.json()

        assert 'detectedLanguage' in response[0], 'Missing detected language ' + response
        assert 'translations' in response[0], 'missing translations ' + response

        detected_language = response[0]['detectedLanguage']['language']
        translated_text = response[0]['translations'][0]['text']

        return translated_text, detected_language

