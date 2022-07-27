import json
from . import log
import os
import sys
required = ['global_loglevel',
               'host',
               'save_folder',
               'checkpoint_path',
               'full_save_path',
               'tensorflow_loglevel',
               'training_shuffle_buffer_size',
               'training_batch_size',
               'model_vocab_size',
               'layers_setup']


def script_path():
    return os.path.abspath(os.path.dirname(__file__))

config_raw = open(script_path()+'/mod.config').read().split('\n')
if '' in config_raw:
    config_raw.remove('')
config_raw = [[y.strip() for y in x.split('=')] for x in config_raw]
log.debug('configurations prepared')

config_list = {}
for i in range(len(config_raw)):
    config_line = config_raw[i]
    a, b = config_line
    if b.isnumeric():
        b = int(b)
    config_list.update({config_line[0]:config_line[1]})
log.debug('configurations proccessed')

del config_raw
del config_line

log.debug('starting parameters validation')
if len(config_list) < len(required):
    log.error('not enough config parameters')
    raise KeyError('not enough config parameters')

required.sort()
current = sorted(list(config_list))
for i in range(len(required)):
    if not (required[i] in current[i]):
        log.error('required config parameter not found: '+required[i])
        raise KeyError('required config parameter not found: '+required[i])
log.debug('parameters validation complete')

