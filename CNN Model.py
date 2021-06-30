''' CNN MODEL '''

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# initializing CNN
classifier = Sequential()

# Step-1 Convolution
#classifier.add(Conv2D(32, 3, 3, input_shape=(48, 48, 1), activation='relu'))
classifier.add(Conv2D(32, 3, 3, input_shape=(64, 64, 3), activation='relu'))

# Step-2 Pooling
classifier.add(MaxPooling2D(pool_size=(2, 2)))

# Adding additional layer
classifier.add(Conv2D(32, 3, 3, activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

# Adding additional layer
classifier.add(Conv2D(32, 3, 3, activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

# Step-3 Flattening
classifier.add(Flatten())

# Step-4 Full Connection
classifier.add(Dense(output_dim=128, activation='relu'))
classifier.add(Dense(output_dim=7, activation='softmax'))

# compile CNN
classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Applying cnn to images
from keras.preprocessing.image import ImageDataGenerator

val_datagen = ImageDataGenerator(rescale=1. / 255)

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    # rotation_range=30,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)
# fill_mode='nearest')

train_generator = train_datagen.flow_from_directory(
    '/home/face-expression-recognition-dataset/images/train',
    target_size=(64, 64),
    batch_size=32,
    # color_mode="grayscale",
    class_mode='categorical')

validation_generator = val_datagen.flow_from_directory(
    '/home/face-expression-recognition-dataset/images/validation',
    target_size=(64, 64),
    batch_size=32,
    # color_mode="grayscale",
    class_mode='categorical')

classifier.fit(train_generator,
               steps_per_epoch=8000,
               epochs=10,
               validation_data=validation_generator,
               validation_steps=7066)

classifier.save('saved_model2.model')
