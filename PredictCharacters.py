import pickle

import SegmentCharacters
import os

def predict_license_plate_number(image_url):
    print("Loading model")
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    filename = os.path.join(__location__, 'finalized_model.sav')
    model = pickle.load(open(filename, 'rb'))

    print('Model loaded. Predicting characters of number plate')
    classification_result = []
    characters, column_list = SegmentCharacters.segment_characters(image_url)
    for each_character in characters:
        # converts it to a 1D array
        each_character = each_character.reshape(1, -1)
        result = model.predict(each_character)
        classification_result.append(result)

    print('Classification result')
    print(classification_result)

    plate_string = ''
    for eachPredict in classification_result:
        plate_string += eachPredict[0]

    print('Predicted license plate')
    print(plate_string)

    # it's possible the characters are wrongly arranged
    # since that's a possibility, the column_list will be
    # used to sort the letters in the right order

    column_list_copy = column_list[:]
    column_list.sort()
    rightplate_string = ''
    for each in column_list:
        rightplate_string += plate_string[column_list_copy.index(each)]

    print('License plate')
    print(rightplate_string)
    return plate_string, rightplate_string
