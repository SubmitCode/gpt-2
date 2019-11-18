import sys, os
sys.path.append('./src')
import settings
import azure_translate
import sample, encoder, model
import os, json
import numpy as np
import tensorflow as tf
from flask import Flask
from flask_restplus import Api, Resource, fields

"""
app = Flask(__name__)
api = Api(
    app, version='1.0', title='GPT-GPU API',
    description='A simple GPT-2 model API which runs on GPU to increase performance',
)

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})
"""


class TodoDAO(object):
    def __init__(self):
        self.azure_translate = azure_translate.AzureTranslate()
        self.tf_session, self.output, self.context = self.prepare_tf_session()


    def get_ai_text(self, sample_input_text:str='Hi how are you?'):
        ''' outputs AI generated text '''
        english_text, detected_language = self.azure_translate.translate_to_english(sample_input_text)        
        english_output_text = self.get_gpt_text(english_text)
        out_text, _ = self.azure_translate.translate(english_output_text, detected_language)
        return out_text


    def prepare_tf_session(
            self,
            seed=None,
            nsamples=1,
            batch_size=1,
            length=None,
            temperature=1,
            top_k=0,
            top_p=1):
        '''calls tensorflow model and returns prediciton'''
        if batch_size is None:
            batch_size = 1
        assert nsamples % batch_size == 0

        models_dir = settings.MODEL_DIR
        model_name = settings.MODEL_NAME 
        hparams = model.default_hparams()
        with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
            hparams.override_from_dict(json.load(f))

        if length is None:
            length = hparams.n_ctx // 2
        elif length > hparams.n_ctx:
            raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)


        sess = tf.Session(graph=tf.Graph())
        sess.__enter__()
        context = tf.placeholder(tf.int32, [batch_size, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)
        output = sample.sample_sequence(
            hparams=hparams, length=length,
            context=context,
            batch_size=batch_size,
            temperature=temperature, top_k=top_k, top_p=top_p
        )

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, model_name))
        saver.restore(sess, ckpt)
        return sess, output, context

        
    def get_gpt_text(self, english_input_text):
        '''calls tensorflow model and returns prediciton'''
        batch_size = 1
        models_dir = settings.MODEL_DIR
        model_name = settings.MODEL_NAME 
        raw_text = english_input_text
        enc = encoder.get_encoder(model_name, models_dir)
        context_tokens = enc.encode(raw_text)
        out = self.tf_session.run(self.output, feed_dict={
            self.context: [context_tokens for _ in range(batch_size)]
        })[:, len(context_tokens):]                    
                
        text = enc.decode(out[0])
        self.tf_session.close()
        return text
                       

   
"""
@ns.route('/<string:input_text>')
class GetAiText(Resource):
    '''outputs a AI generated text give the input language'''
    def __init__(self):
        self.DAO = TodoDAO()

    @ns.doc('outputs a GPT-2 generated text')
    @ns.marshal_with(todo)
    @ns.param('input_text', 'text input in different languages')
    def get(self, input_text):
        '''List all tasks'''
        text = self.DAO.get_ai_text(input_text)
        return { 'text': text }


#if __name__ == '__main__':
#    app.run(debug=True)
    #aitxt = GetAiText()
    #out = aitxt.get("test input als deutscher Text.")
"""