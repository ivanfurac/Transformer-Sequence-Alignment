from positionalembeddinglayer import PositionalEmbeddingLayer
from encoderlayer import EncoderLayer
from decoderlayer import DecoderLayer

import tensorflow as tf

class TransformerModel(tf.keras.Model):
    def __init__(self,
                 input_vocab_size,
                 output_vocab_size,
                 input_sequence_length,
                 output_sequence_length,
                 embed_dim,
                 dense_dim,
                 num_heads,
                 num_layers,
                 dropout_rate,
                 **kwargs):
        super(TransformerModel, self).__init__(**kwargs)
        
        self.encoder_embedding = PositionalEmbeddingLayer(input_sequence_length, input_vocab_size, embed_dim, dropout_rate)
        self.encoder_layers = [EncoderLayer(input_sequence_length, embed_dim, dense_dim, num_heads, dropout_rate) for _ in range(num_layers)]
        
        self.decoder_embedding = PositionalEmbeddingLayer(output_sequence_length, output_vocab_size, embed_dim, dropout_rate)
        self.decoder_layers = [DecoderLayer(output_sequence_length, embed_dim, dense_dim, num_heads, dropout_rate) for _ in range(num_layers)]
        self.final_layer = tf.keras.layers.Dense(output_vocab_size)
        
    def padding_mask(self, input):
        mask = tf.math.not_equal(input, 0)
        mask = tf.cast(mask, tf.float32)
        return mask[:, tf.newaxis, tf.newaxis, :]
    
    def lookahead_mask(self, shape):
        mask = tf.linalg.band_part(tf.ones((shape, shape)), -1, 0) 
        return mask
    
    def encoder(self, encoder_input, training=False):
        encoder_padding_mask = self.padding_mask(encoder_input)
        
        encoder_output = self.encoder_embedding(encoder_input, training)
        for layer in self.encoder_layers:
            encoder_output = layer(encoder_output, encoder_padding_mask, training)
        return encoder_output, encoder_padding_mask
    
    def decoder(self, decoder_input, encoder_output, encoder_padding_mask, training=False):
        decoder_padding_mask = self.padding_mask(decoder_input)
        decoder_lookahead_mask = self.lookahead_mask(decoder_input.shape[1])
        decoder_lookahead_mask = tf.minimum(decoder_padding_mask, decoder_lookahead_mask)
        
        decoder_output = self.decoder_embedding(decoder_input, training)
        for layer in self.decoder_layers:
            decoder_output = layer(decoder_output, encoder_output, encoder_padding_mask, decoder_lookahead_mask, training)
            
        decoder_output = self.final_layer(decoder_output)  
        return decoder_output
        
    def call(self, inputs, training=False):
        encoder_input = inputs[0]
        decoder_input = inputs[1]     
        
        #encoding_layer
        encoder_output, encoder_padding_mask = self.encoder(encoder_input, training)        
            
        #decoding_layer
        decoder_output = self.decoder(decoder_input, encoder_output, encoder_padding_mask)
              
        return decoder_output