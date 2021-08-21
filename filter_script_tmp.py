import numpy as np
import os
checkpoint_path = "models/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
import tensorflow_datasets as tfds
import tensorflow as tf
from imap_tools import MailBox, AND
tfds.disable_progress_bar()
server = "imap.gmail.com"
model = ''
db = ''
import subprocess
import base64
import logging
import os
import hashlib
from random import SystemRandom

from cryptography.exceptions import AlreadyFinalized
from cryptography.exceptions import InvalidTag
from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC



def encrypt_to_base64(text, key):
        key = hashlib.sha256(key.encode("utf-8")).digest()
        password_bytes = key
        aesgcm = AESGCM(password_bytes)
        cipher_text_bytes = aesgcm.encrypt(
            nonce=b'abcdefgh',
            data=text.encode('utf-8'),
            associated_data=None
        )
        return base64.urlsafe_b64encode(cipher_text_bytes)


def decrypt_from_base64(text, key):
        key = hashlib.sha256(key.encode("utf-8")).digest()
        password_bytes = key
        aesgcm = AESGCM(password_bytes)
        decrypted_cipher_text_bytes = aesgcm.decrypt(
            nonce=b'abcdefgh',
            data=base64.urlsafe_b64decode(text),
            associated_data=None
        )
        return decrypted_cipher_text_bytes.decode('utf-8')

def build_from_emails():
    texts = []
    ids = []
    cpuinfo = subprocess.run(['cat','/proc/cpuinfo'], capture_output=True)
    uid = str(cpuinfo.stdout)
    if not(os.path.isfile('db')):
        print('\nLogin information file not found, creating one for you.')
        login = input('Enter gmail box login(will be saved for further use)(example: example@gmail.com): ')
        password = input('Enter password(stored in encrypted state): ')
        spec_mail = input('Specify email to accept samples from(necessary): ')
        with open('db','w') as db:
            db.write(login+'\n'+spec_mail)
        with open('pass','wb') as passw:
            passw.write(encrypt_to_base64(password, uid))
    elif os.path.isfile('db'):
        with open('db','r') as db:
            db_array = db.readlines()
        login = db_array[0]
        spec_mail = db_array[1]
        with open('pass','rb') as passw:
            print(passw.read())
            password = decrypt_from_base64(passw.read(), uid)

    if not(spec_mail):
        spec_mail = None

    mb = MailBox(server).login(login, password)
    messages = mb.fetch(criteria=AND(seen=False, from_=spec_mail),
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
    BUFFER_SIZE = 10000
    BATCH_SIZE = 128
    train_dataset = train_dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

    VOCAB_SIZE = 1000
    encoder = tf.keras.layers.experimental.preprocessing.TextVectorization(
        max_tokens=VOCAB_SIZE)
    encoder.adapt(train_dataset.map(lambda text, label: text))
    vocab = np.array(encoder.get_vocabulary())
    vocab[:20]
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
        history = model.fit(train_dataset, epochs=int(input('Number of epochs: ')),
                        callbacks=[cp_callback])
    except KeyboardInterrupt:
        print('Keyboard interrupt')
    return model

if os.path.isdir('models'):
    if input('Rebuild filter model?(y/N)')=='y':
        model = build_from_emails()
    else:
        print('Leaving everything as is')
else:
    build_from_emails()

if model:
    print('Model updated(you can try it or stop builder with Ctrl+C)')
    while True:
        pred = model.predict(np.array([input('Text to predict from: ')]))
        print(pred[0])
