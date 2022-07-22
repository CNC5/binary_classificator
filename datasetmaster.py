import credmaster
import numpy as np
import tensorflow_datasets as tfds
import tensorflow as tf
import mailmaster

def generate():
	ids = []
	texts = []
	credentials = credmaster.get_creds()
	login, password, spec_mail = credentials
	mailfetcher = mailmaster.fetcher()
	mailfetcher.login(login, password)
	messages = mailfetcher.fetch(spec_mail)
	for msg in messages:
		text = msg.text
		texts.append(text)
		ids.append(int(msg.subject))

	ids = tf.cast(ids, tf.int64)
	train_dataset = tf.data.Dataset.from_tensor_slices((texts,ids))
	train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)
	BUFFER_SIZE = 10000
	BATCH_SIZE = 128
	train_dataset = train_dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
	print('Dataset loaded and processed')
	return train_dataset

if __name__ == '__main__':
	test_dataset = generate()
	if test_dataset:
		print('Dataset gen OK: ',type(test_dataset))

