import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def get_threshold(image):
    a, b, x = plt.hist(image.flatten())
    arg = np.argmax(a)
    threshold = [b[arg], b[arg+1]]
    plt.clf()
    return threshold


def make_mask(path, color='blue', print_plot=False):
    image = Image.open(path)
    image = image.resize((150, 150))
    image = image.convert('L')
    image = np.array(image)
    threshold = get_threshold(image)
    if color == 'blue':
        n = [0, 0, 255]
    masked_image = []
    for i in image.flatten():
        if i >= threshold[0] and i <= threshold[1]:
            masked_image.append(255)
        else:
            masked_image.append(0)
    masked_image = np.array(masked_image)
    masked_image = masked_image.reshape(image.shape)
    if print_plot == True:
        plt.imshow(masked_image)
    return masked_image


def make_predictions(path, model):
    labels = ['Cats', 'Dogs']
    print('The masked image is :')
    arr = make_mask(path, print_plot=False)
    arr = np.array(arr)
    arr = arr.reshape(1, 150, 150)
    clas = np.argmax(model.predict(arr), axis=-1)
    # plt.imshow(Image.open(path))
    return labels[clas[0]]


# def predict_for_accuracy(path, model):
#     labels = ['Cats', 'Dogs']
#     # print('The masked image is :')
#     arr = make_mask(path, print_plot=True)
#     arr = np.array(arr)
#     arr = arr.reshape(1, 150, 150)
#     clas = np.argmax(model.predict(arr), axis=-1)
#     return labels[clas[0]]


# training_data_path = 'C:/Users/Ala/Documents/dog vs cat/dataset/test_set/dogs'

# filenames = [f for f in os.listdir(training_data_path) if os.path.isfile(
#     os.path.join(training_data_path, f))]

# successful_predictions = 0

# for filename in filenames[:1000]:
#     predicted_class = predict_for_accuracy(
#         f"{training_data_path}/{filename}", model)

#     if predicted_class == "Dogs":
#         successful_predictions += 1

# print(f"Accuracy is: {(successful_predictions / 1000) * 100} %")

# make_predictions(
#     'C:/Users/Ala/Downloads/Zrzut ekranu 2022-01-20 224810.jpg', model)
