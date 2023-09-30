import tensorflow as tf
import numpy as np

class PositionalEmbeddingLayer(tf.keras.layers.Layer):
    def __init__(self, sequence_length, vocab_size, embed_dim, dropout_rate, **kwargs):
        super(PositionalEmbeddingLayer, self).__init__(**kwargs)
        self.sequence_length = sequence_length
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim        
        
        self.token_embeddings = tf.keras.layers.Embedding(
            input_dim=vocab_size, output_dim=embed_dim
        )
        self.embedded_positions = self.generate_positional_encoding()
        self.dropout = tf.keras.layers.Dropout(dropout_rate)
        
    def generate_positional_encoding(self, n = 10000):
        encodings = np.zeros((self.sequence_length, self.embed_dim))
        for pos in range(self.sequence_length):
            for i in range(int(self.embed_dim/2)):
                denominator = n ** ((2*i) / (self.embed_dim))
                encodings[pos, 2*i] = np.sin(pos / denominator)
                encodings[pos, 2*i + 1] = np.cos(pos / denominator)
                
        return tf.cast(encodings, dtype=tf.float32)[tf.newaxis, :, :]        

    def call(self, inputs, training=False):
        embedded_tokens = self.token_embeddings(inputs)
        embedded_tokens *= tf.math.sqrt(tf.cast(self.embed_dim, dtype=tf.float32))
        output = embedded_tokens + self.embedded_positions
        return self.dropout(output, training=training)