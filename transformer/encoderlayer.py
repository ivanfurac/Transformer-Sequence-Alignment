import tensorflow as tf

class EncoderLayer(tf.keras.layers.Layer):
    def __init__(self, sequence_length, embed_dim, dense_dim, num_heads, droput_rate, **kwargs):
        super(EncoderLayer, self).__init__(**kwargs)
        self.build(input_shape=[None, sequence_length, embed_dim])
        self.embed_dim = embed_dim
        self.dense_dim = dense_dim
        self.num_heads = num_heads
        self.sequence_length = sequence_length
        
        #first sub-layer
        self.attention = tf.keras.layers.MultiHeadAttention(
            num_heads=num_heads, key_dim=embed_dim
        )
        self.dropout1 = tf.keras.layers.Dropout(droput_rate)
        self.layernorm1 = tf.keras.layers.LayerNormalization()
        
        #second sub-layer
        self.feed_forward = tf.keras.Sequential(
            [tf.keras.layers.Dense(dense_dim, activation="relu"), tf.keras.layers.Dense(embed_dim)]
        )
        self.dropout2 = tf.keras.layers.Dropout(droput_rate)
        self.layernorm2 = tf.keras.layers.LayerNormalization()

    def call(self, inputs, padding_mask, training=False):
        attention_output = self.attention(query=inputs, value=inputs, key=inputs, attention_mask=padding_mask)
        attention_output = self.dropout1(attention_output, training=training)
        proj_input = self.layernorm1(inputs + attention_output)
        proj_output = self.feed_forward(proj_input)
        proj_output = self.dropout2(proj_output, training=training)
        return self.layernorm2(proj_input + proj_output)