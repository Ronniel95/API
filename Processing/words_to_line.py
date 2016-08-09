import pytesseract
from PIL import Image


def recog_words_on_line(words, wordLines, im):
    word_lists_per_line = [] # array of sub_arrays, sub_array includes images, correspond to line
    word_id = wordLines[0]
    word_list = []
    for i, id in enumerate(wordLines):
        # converting to PILimage, because tesseract wants only this
        pil_im = Image.fromarray(im[(words[i][1]-1):(words[i][1]+words[i][3]+1), (words[i][0]-1):(words[i][0]+words[i][2]+1)])
        if id == word_id:
            word_list.append(pytesseract.image_to_string(pil_im, "ukr"))
        else:
            word_id = id
            word_lists_per_line.append(word_list)
            word_list = [pytesseract.image_to_string(pil_im, "ukr")]
    word_lists_per_line.append(word_list)
    return word_lists_per_line

def write_txt_bill_recognition(file_name, words_lists_per_line):
    with open(file_name, mode="w") as f:
        for words in words_lists_per_line:
            f.write("; ".join(words) + '\n')

