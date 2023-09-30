import tensorflow as tf

class LRScheduler(tf.keras.optimizers.schedules.LearningRateSchedule):
    def __init__(self, embed_dim, warmup_steps=4000, **kwargs):
        super(LRScheduler, self).__init__(**kwargs)
        
        self.embed_dim = tf.cast(embed_dim, tf.float32)
        self.warmup_steps = tf.cast(warmup_steps, tf.float32)
        
    def __call__(self, step_num):
        step_num = tf.cast(step_num, tf.float32)
        arg1 = tf.math.rsqrt(self.embed_dim)
        arg2 = tf.math.rsqrt(step_num)
        arg3 = step_num * (self.warmup_steps ** -1.5) 
        return arg1 * tf.math.minimum(arg2, arg3)