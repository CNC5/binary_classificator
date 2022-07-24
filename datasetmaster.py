import credmaster
import numpy as np
import tensorflow_datasets as tfds
import tensorflow as tf
import mailmaster

def generate():
	ids = []
	texts = []
	credentials = credmaster.get_creds()
	login, atoken, spec_mail = credentials
	mailfetcher = mailmaster.fetcher()
	mailfetcher.login(login, atoken)
	messages = mailfetcher.fetch(spec_mail)
	mailfetcher.logout()
	del mailfetcher
	print(messages)
	for message in messages:
		text = message[1]

		texts.append(text)
		ids.append(int(message[0]))

	ids = tf.cast(ids, tf.int64)
	print(ids, '\n', texts)
	train_dataset = tf.data.Dataset.from_tensor_slices((texts,ids))
	train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)
	BUFFER_SIZE = 10000
	BATCH_SIZE = 128
	train_dataset = train_dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE).prefetch(min(len(train_dataset)//2, 100))
	print('Dataset loaded and processed')
	return train_dataset

if __name__ == '__main__':
	test_dataset = generate()
	if test_dataset:
		print('Dataset gen OK: ',type(test_dataset), '\n', test_dataset)
	else:
		print('Dataset gen failure')
