from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint  # ModelCheckpointをインポート

# パラメータ
img_height = 224
img_width = 224
batch_size = 32
data_dir = "/content/drive/MyDrive/SSH_Blackboard_AI/BlackboardYN/"

# データ拡張
train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    validation_split=0.2  # 20%を検証用
)

# データジェネレータ
train_generator = train_datagen.flow_from_directory(
    data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary',  # ラベルを0または1にする
    subset='training',
)

validation_generator = train_datagen.flow_from_directory(
    data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary',  # ラベルを0または1にする
    subset='validation',
)

# モデル構築
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')  # 出力を1ユニットに
])

# モデルコンパイル
model.compile(optimizer='adam',
              loss='binary_crossentropy',  # 2クラス分類
              metrics=['accuracy'])

# ModelCheckpointの設定
checkpoint = ModelCheckpoint(
    filepath="blackboardYN_model.h5",  # 保存先のファイル名
    monitor="val_loss",    # モニタリングする指標
    save_best_only=True,       # 最良モデルのみ保存
    save_weights_only=False,   # モデル全体を保存（重みだけではない）
    verbose=1                  # 保存時にメッセージを表示
)

# モデルの訓練
history = model.fit(
    train_generator,
    epochs=10,
    validation_data=validation_generator,
    callbacks=[checkpoint]  # ModelCheckpointをコールバックに追加
)
