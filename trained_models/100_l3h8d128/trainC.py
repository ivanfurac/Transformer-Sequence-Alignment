import tensorrt
import keras_nlp
import tensorflow as tf
from transformer import TransformerModel
from lrscheduler import LRScheduler

### DATA PATHS ###

train_data_path = '../alignments_100_200/pairs/gap5/alignments_200_gap5_100000'
input_vocab = '../vocab/spaces_vocab'
output_vocab = '../vocab/pairs_vocab'
save_model_path = '100_l3h8d128/model.ckpt'

### TRAINING PARAMETERS ###

val_dataset_size = 0.1
batch_size = 32
num_epochs = 100
beta1 = 0.9
beta2 = 0.98
epsilon = 1e-9

### MODEL PARAMETERS ###

input_sequence_length = 403
output_sequence_length = 402
embed_dim = 128
dense_dim = 512
num_heads = 8
num_layers = 3
dropout_rate = 0.3

### DATA PREPROCESSING ###

pairs = []

file = open(train_data_path, 'r')
for _, line in enumerate(file):
    unaligned, aligned, score = line.strip('\n').split('\t')
    unaligned = 'START ' + unaligned + ' END'
    aligned = 'START ' + aligned + ' END'
    pairs.append((unaligned, aligned))
file.close()

print('DONE WITH READING PAIRS')

num_train = int((1 - val_dataset_size)*len(pairs)) 
train_pairs = pairs[:num_train]
val_pairs = pairs[num_train:len(pairs)]

input_tokenizer = keras_nlp.tokenizers.WordPieceTokenizer(
    vocabulary = input_vocab,
    sequence_length = input_sequence_length,
    oov_token = 'UNK'
)
input_vocab_size = input_tokenizer.vocabulary_size()

output_tokenizer = keras_nlp.tokenizers.WordPieceTokenizer(
    vocabulary = output_vocab,
    sequence_length = output_sequence_length + 1,
    oov_token = 'UNK'
)
output_vocab_size = output_tokenizer.vocabulary_size()

def format_dataset(unaligned, aligned):
    unaligned = input_tokenizer(unaligned)
    aligned = output_tokenizer(aligned)
    return ((unaligned, aligned[:, :-1]), aligned[:, 1:])

def make_dataset(pairs):
    unaligned, aligned = zip(*pairs)
    unaligned = list(unaligned)
    aligned = list(aligned)
    dataset = tf.data.Dataset.from_tensor_slices((unaligned, aligned))
    dataset = dataset.batch(batch_size)
    dataset = dataset.map(format_dataset)
    return dataset.shuffle(len(pairs)).prefetch(16)

train_ds = make_dataset(train_pairs)

print('DONE WITH PREPARING TRAIN DATA')

val_ds = make_dataset(val_pairs)

print('DONE WITH PREPARING VALIDATION DATA')

print('PREPROCESSING DONE!')

### INITIALIZING A MODEL ###

model = TransformerModel(input_vocab_size,
                         output_vocab_size,
                         input_sequence_length,
                         output_sequence_length,
                         embed_dim,
                         dense_dim,
                         num_heads,
                         num_layers,
                         dropout_rate)

print('Testing model output:')
test_data = val_ds.take(1).get_single_element()
output = model(test_data[0])
print(output.shape)
model.summary()

### INITIALIZE LR SCHEDULER AND OPTIMIZER

optimizer = tf.keras.optimizers.Adam(LRScheduler(embed_dim), beta1, beta2, epsilon)

### DEFINE LOSS AND ACCURACY FUNCTIONS ###

def loss_function(target, prediction):
    padding_mask = tf.math.not_equal(target, 0)
    padding_mask = tf.cast(padding_mask, tf.float32)
    
    loss_obj = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True, reduction='none')
    loss = loss_obj(target, prediction) * padding_mask
    
    return tf.reduce_sum(loss)/tf.reduce_sum(padding_mask)

def accuracy_function(target, prediction):
    predictions = tf.argmax(prediction, axis=-1)
    targets = tf.cast(target, predictions.dtype)
    
    padding_mask = tf.math.not_equal(target, 0)
    accuracy = tf.math.equal(targets, predictions)    
    accuracy = tf.math.logical_and(padding_mask, accuracy)
    padding_mask = tf.cast(padding_mask, tf.float32)
    accuracy = tf.cast(accuracy, tf.float32)
    
    return tf.reduce_sum(accuracy)/tf.reduce_sum(padding_mask)

### START TRAINING ###

model.compile(loss=loss_function, optimizer=optimizer, metrics=[accuracy_function])

checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath = save_model_path,
    save_weights_only = True,
    monitor = 'val_loss',
    mode = 'min',
    save_best_only = True    
)

model.fit(train_ds, epochs=num_epochs, validation_data=val_ds, callbacks=[checkpoint_callback], verbose=2)