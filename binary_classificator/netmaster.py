import numpy as np
import os
checkpoint_path = 'models/cp.ckpt'
checkpoint_dir = os.path.dirname(checkpoint_path)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from . import log


def build_model(train_dataset):
	VOCAB_SIZE = 1000
	encoder = tf.keras.layers.experimental.preprocessing.TextVectorization(
		max_tokens=VOCAB_SIZE)
	encoder.adapt(train_dataset.map(lambda text, label: text))
	vocab = np.array(encoder.get_vocabulary())

	log.debug('neural network model build started')
	model = tf.keras.Sequential([
                encoder,
                tf.keras.layers.Embedding(
                    input_dim=len(encoder.get_vocabulary()),
                    output_dim=64,
                    mask_zero=True),
		tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
		tf.keras.layers.Dense(64, activation='relu'),
		tf.keras.layers.Dense(1)
	])
	log.debug('neural network build complete')

	cp_callback = tf.keras.callbacks.ModelCheckpoint(
		filepath=checkpoint_path,
		save_weights_only=True,
		verbose=1)

	model.compile(
		loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
		optimizer=tf.keras.optimizers.Adam(1e-4),
		metrics=['accuracy'],
		run_eagerly=False)

	log.debug('neural network training starting')
	model.fit(train_dataset, epochs=int(input('Number of epochs: ')),callbacks=[cp_callback])
	log.debug('neural network training complete')
	model.predict(['text'])
	log.debug('neural network initial test succesfull')
	model.save('models/full_model')
	log.debug('neural network model saved')


class binary_predictor():
	def __init__(self, model):
		self.model = model
		log.debug('neural network model loaded')

	def predict(self, text):
		prediction = self.model.predict([text])
		log.debug('prediction done')
		return prediction[0][0]


def create_predictor():
	if os.path.isdir('models'):
		model = tf.keras.models.load_model('models/full_model')
		return binary_predictor(model)
	else:
		log.error('models folder not found')
		raise FileNotFoundError
