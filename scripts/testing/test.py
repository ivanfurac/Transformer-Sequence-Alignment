#import tensorrt
import tensorflow as tf
import keras_nlp
from transformer import TransformerModel
from metrics_spaces import accuracy, coverage, alignment_score

### PATHS ###

test_data = 'C:/Users/Ivan/Desktop/CODE/HemoAlign/alignments_200_gap5_test_spaces'
model_path = 'C:/Users/Ivan/Desktop/CODE/models/spaces_l2h8d128/model.ckpt'
input_voc_path = 'C:/Users/Ivan/Desktop/CODE/vocab/spaces_vocab'
output_voc_path = 'C:/Users/Ivan/Desktop/CODE/vocab/spaces_output_vocab'

### MODEL PARAMETERS ###

input_sequence_length = 403
output_sequence_length = 802
embed_dim = 128
dense_dim = 512
num_heads = 8
num_layers = 2
dropout_rate = 0.3

input_tokenizer = keras_nlp.tokenizers.WordPieceTokenizer(
    vocabulary = input_voc_path,
    sequence_length = input_sequence_length,
    oov_token = 'UNK'
)
input_vocab_size = input_tokenizer.vocabulary_size()

output_tokenizer = keras_nlp.tokenizers.WordPieceTokenizer(
    vocabulary = output_voc_path,
    sequence_length = output_sequence_length + 1,
    oov_token = 'UNK'
)
output_vocab_size = output_tokenizer.vocabulary_size()

model = TransformerModel(input_vocab_size,
                         output_vocab_size,
                         input_sequence_length,
                         output_sequence_length,
                         embed_dim,
                         dense_dim,
                         num_heads,
                         num_layers,
                         dropout_rate)

print('LOADING MODEL...')

model.load_weights(model_path).expect_partial()

print('MODEL LOADED!')

file = open(test_data, 'r')
lines = file.readlines()
file.close()

print('TEST DATA READING COMPLETED')
print('OUTPUT GENERATION STARTS')

for line in lines:
    unaligned, aligned, score = line.strip('\n').split('\t')
    
    seq1 = unaligned.split('|')[0].strip(' ').replace(' ', '')
    seq2 = unaligned.split('|')[1].strip(' ').replace(' ', '')
    
    unaligned = 'START ' + unaligned + ' END'    
    encoder_input = input_tokenizer([unaligned])
    decoder_input = 'START'
    
    encoder_output, encoder_padding_mask = model.encoder(encoder_input)
    
    for i in range(output_sequence_length):
        tokenized_decoder_input = output_tokenizer([decoder_input])[:, :-1]
        predictions = model.decoder(tokenized_decoder_input, encoder_output, encoder_padding_mask)
        
        new_token_index = tf.argmax(predictions[0, i, :])
        
        new_token = output_tokenizer.vocabulary[new_token_index]
        
        if(new_token == 'END'):
            break
        
        decoder_input = decoder_input + ' ' + new_token
    
    output_split = decoder_input.split(' ')[1:]
    target_split = aligned.split(' ')
    
    acc = accuracy(output_split, target_split)
    (coverage1, coverage2) = coverage(output_split, seq1, seq2)
    try:
        al_score = alignment_score(output_split)  
    except:
        print('ERROR.')
        continue
    
    print(str(acc) + '\t' + str(coverage1) + '\t' + str(coverage2) + '\t' + str(score) + '\t' + str(al_score))