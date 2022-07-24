import numpy as np
import os
checkpoint_path = "models/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
import tensorflow_datasets as tfds
import tensorflow as tf
tfds.disable_progress_bar()


def build_model(train_dataset):
	VOCAB_SIZE = 1000
	encoder = tf.keras.layers.experimental.preprocessing.TextVectorization(
		max_tokens=VOCAB_SIZE)
	encoder.adapt(train_dataset.map(lambda text, label: text))
	vocab = np.array(encoder.get_vocabulary())
	print(vocab[:20])

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

	cp_callback = tf.keras.callbacks.ModelCheckpoint(
		filepath=checkpoint_path,
		save_weights_only=True,
		verbose=1)

	model.compile(
		loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
		optimizer=tf.keras.optimizers.Adam(1e-4),
		metrics=['accuracy'],
		run_eagerly=False)

	model.fit(train_dataset, epochs=int(input('Number of epochs: ')),callbacks=[cp_callback])
	model.predict(['text'])
	model.save('models/full_model')


class binary_predictor():
	def __init__(self):
		self.model = tf.keras.models.load_model('models/full_model')

	def predict(self, text):
		return self.model.predict([text])
