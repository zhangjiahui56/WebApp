from keras import backend as K
from keras import layers as LL
from keras.regularizers import l1,l2,Regularizer
from keras.engine.topology import Layer
from keras.engine.saving import load_weights_from_hdf5_group_by_name
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.merge import Maximum,Concatenate as Concat
from keras.applications import resnet50
from keras.applications.resnet50 import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.optimizers import Adam
from keras.losses import mean_squared_error
from keras.callbacks import EarlyStopping,ModelCheckpoint,CSVLogger

def LeafCountingModel():
    layers = resnet50.ResNet50(include_top=False, weights='imagenet', input_shape=(240, 240, 3))
    layers.trainable = False
    for layer in layers.layers[-20:]:
        layer.trainable = True
    x = layers.output
    x = LL.Flatten(name='rgb_flatten')(x)
    x = LL.core.Dense(1024, activation='relu')(x)
    x = LL.core.Dense(512, activation='relu', activity_regularizer=l2(0.01))(x)
    output = LL.core.Dense(1)(x)
    model = Model(inputs=layers.input, outputs=output)

    model.compile(optimizer=Adam(lr=0.0001), loss=mean_squared_error, metrics=['mse'])

    # model.load_weights('model_weighs/model_125_ver5.h5')

    return model


