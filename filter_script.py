import numpy as np
import os
checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
import tensorflow_datasets as tfds
import tensorflow as tf
from imap_tools import MailBox, AND
tfds.disable_progress_bar()

texts=[]
ids=[]

ORG_EMAIL   = "@gmail.com"
user = "user" + ORG_EMAIL
password = "password"
server = "imap.gmail.com"

mb = MailBox(server).login(user, password)
messages = mb.fetch(criteria=AND(seen=True, from_="specific@mail"),
                        mark_seen=False,
                        bulk=True)

for msg in messages:
    print(msg.from_, ': ', msg.subject)
    text = msg.text
    texts.append(text)
    ids.append(int(msg.subject))

ids = tf.cast(ids, tf.int64)
train_dataset = tf.data.Dataset.from_tensor_slices((texts,ids))
train_dataset = train_dataset.prefetch(1)

print('Dataset loaded and processed')
for example, label in train_dataset.take(1):
  print('text: ', example.numpy())
  print('label: ', label.numpy())
BUFFER_SIZE = 10000
BATCH_SIZE = 128
train_dataset = train_dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

VOCAB_SIZE = 1000
encoder = tf.keras.layers.experimental.preprocessing.TextVectorization(
    max_tokens=VOCAB_SIZE)
encoder.adapt(train_dataset.map(lambda text, label: text))
vocab = np.array(encoder.get_vocabulary())
vocab[:20]
encoded_example = encoder(example)[:3].numpy()
encoded_example
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

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)


model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])
try:
    history = model.fit(train_dataset, epochs=int(input('Number of epochs:')),
                    callbacks=[cp_callback])
except KeyboardInterrupt:
    print('Keyboard interrupt')

test_loss, test_acc = model.evaluate(train_dataset)

print('Test Loss:', test_loss)
print('Test Accuracy:', test_acc)


while True:
    pred = model.predict(np.array([input('Text to predict from: ')]))
    print(pred[0])
