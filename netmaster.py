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
	vocab[:20]

	model = tf.keras.Sequential([
		tf.keras.layers.Conv2D(input_shape = tf.data.AUTOTUNE, 
			filters = tf.data.AUTOTUNE, kernel_size = (5, 5), 
			activation = "relu"),
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
		run_eagerly=True)

	try:
		model.fit(train_dataset, epochs=int(input('Number of epochs: ')),callbacks=[cp_callback])
	except KeyboardInterrupt:
		print('Keyboard interrupt')
	return model
