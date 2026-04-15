import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt

def create_model(input_shape=(256, 256, 3)):
    """
    Creates and compiles a CNN model for anemia detection.
    """
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(256, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5), # Regularization to reduce overfitting
        Dense(1, activation='sigmoid')
    ])

    model.compile(
        loss='binary_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )
    return model

def plot_history(history, save_path="training_history.png"):
    """
    Plots training and validation accuracy/loss.
    """
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(acc) + 1)

    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(epochs, acc, 'b', label='Training accuracy')
    plt.plot(epochs, val_acc, 'r', label='Validation accuracy')
    plt.title('Training and Validation Accuracy')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss, 'b', label='Training loss')
    plt.plot(epochs, val_loss, 'r', label='Validation loss')
    plt.title('Training and Validation Loss')
    plt.legend()

    plt.savefig(save_path)
    print(f"Training history plot saved to {save_path}")

def main():
    # Directories
    base_dir = os.path.join('..', 'data')
    if not os.path.exists(base_dir):
        # Fallback to local dir if running from different pwd
        base_dir = 'data'
        
    print(f"Using dataset directory: {base_dir}")

    # Parameters
    img_width, img_height = 256, 256
    batch_size = 32
    epochs = 100

    # Data Augmentation & Generators
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2
    )

    print("Loading Training Data...")
    train_generator = train_datagen.flow_from_directory(
        base_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='binary',
        subset='training'
    )

    print("Loading Validation Data...")
    validation_generator = train_datagen.flow_from_directory(
        base_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='binary',
        subset='validation'
    )

    # Callbacks for robust training
    callbacks = [
        # Save the best model
        ModelCheckpoint('best_anemia_cnn_model.keras', save_best_only=True, monitor='val_accuracy', mode='max'),
        # Stop early if validation loss plateaus
        EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
        # Reduce learning rate when validation loss plateaus
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6, verbose=1)
    ]

    # Initialize model
    model = create_model(input_shape=(img_width, img_height, 3))
    model.summary()

    # Train
    print("Starting training process...")
    history = model.fit(
        train_generator,
        steps_per_epoch=max(1, train_generator.samples // batch_size),
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=max(1, validation_generator.samples // batch_size),
        callbacks=callbacks
    )

    # Save final model state and plot training history
    model.save('final_anemia_cnn_model.keras')
    print("Final model saved as final_anemia_cnn_model.keras")
    
    plot_history(history)

if __name__ == "__main__":
    main()
