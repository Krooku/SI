import numpy
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
import os.path
from theano.tensor.nnet import conv2d

class neuralnetwork():
    classifier = Sequential()
    training_set = ImageDataGenerator()
    def __init__(self):
        self.classifier.add(Convolution2D(32, 3, 3, input_shape=(64, 64, 3), activation='relu'))
        self.classifier.add(MaxPooling2D(pool_size=(2, 2)))
        self.classifier.add(Convolution2D(32, 3, 3, activation='relu'))
        self.classifier.add(MaxPooling2D(pool_size=(2, 2)))
        self.classifier.add(Flatten())
        # pelne podlaczene
        self.classifier.add(Dense(output_dim=128, activation='relu'))
        self.classifier.add(Dense(output_dim=1, activation='sigmoid'))
        self.classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        # modyfikacja danych
        train_datagen = ImageDataGenerator(rescale=1. / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        test_datagen = ImageDataGenerator(rescale=1. / 255)
        self.training_set = train_datagen.flow_from_directory('images/dataset/training_set', target_size=(64, 64),
                                                              batch_size=32, class_mode='binary')
        test_set = test_datagen.flow_from_directory('images/dataset/test_set', target_size=(64, 64), batch_size=32,
                                                    class_mode='binary')

        if (os.path.isfile('tr.h5')):
            self.classifier.load_weights('tr.h5')
        else:
            self.classifier.fit_generator(self.training_set, steps_per_epoch=210, epochs=2, validation_data=test_set, validation_steps=800)
            self.classifier.save('tr.h5', True)

    def recognize(self, name):
        test_image = image.load_img(name, target_size=(64, 64))
        test_image = image.img_to_array(test_image)
        test_image = numpy.expand_dims(test_image, axis=0)
        result = self.classifier.predict(test_image)
        self.training_set.class_indices

        if result[0][0] >= 0.5:
            prediction = 'nie bomba'
            print(prediction)
            print(result)
            return False
        else:
            prediction = 'bomba'
            print(prediction)
            print(result)
            return True
