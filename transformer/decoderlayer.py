import tensorflow as tf

class DecoderLayer(tf.keras.layers.Layer):
    def __init__(self, sequence_length, embed_dim, dense_dim, num_heads, dropout_rate, **kwargs):
        super(DecoderLayer, self).__init__(**kwargs)
        self.build(input_shape=[None, sequence_length, embed_dim])
        self.embed_dim = embed_dim
        self.dense_dim = dense_dim
        self.num_heads = num_heads
        self.sequence_length = sequence_length
        
        #first sub-layer
        self.attention1 = tf.keras.layers.MultiHeadAttention(
            num_heads=num_heads, key_dim=embed_dim
        )
        self.dropout1 = tf.keras.layers.Dropout(dropout_rate)
        self.layernorm1 = tf.keras.layers.LayerNormalization()
        
        #second sub-layer
        self.attention2 = tf.keras.layers.MultiHeadAttention(
            num_heads=num_heads, key_dim=embed_dim
        )
        self.dropout2 = tf.keras.layers.Dropout(dropout_rate)
        self.layernorm2 = tf.keras.layers.LayerNormalization()
        
        #third sub-layer        
        self.feed_forward = tf.keras.Sequential(
            [tf.keras.layers.Dense(dense_dim, activation="relu"), tf.keras.layers.Dense(embed_dim)]
        )
        self.dropout3 = tf.keras.layers.Dropout(dropout_rate)        
        self.layernorm3 = tf.keras.layers.LayerNormalization()

    def call(self, inputs, encoder_outputs, padding_mask, lookahead_mask, training=False):
        attention_output_1 = self.attention1(query=inputs, value=inputs, key=inputs, attention_mask=lookahead_mask)
        attention_output_1 = self.dropout1(attention_output_1, training=training)
        attention_output_1 = self.layernorm1(inputs + attention_output_1)

        attention_output_2 = self.attention2(query=attention_output_1, value=encoder_outputs, key=encoder_outputs, attention_mask=padding_mask)
        attention_output_2 = self.dropout2(attention_output_2, training=training)
        attention_output_2 = self.layernorm2(attention_output_1 + attention_output_2)
        
        proj_output = self.feed_forward(attention_output_2)
        proj_output = self.dropout3(proj_output, training=training)
        return self.layernorm3(attention_output_2 + proj_output)