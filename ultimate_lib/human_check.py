import numpy as np
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
from flask import render_template

"""
To check the human input

Randomly make a math question (the number is an integer between 0 and 99, +, - only)
Transform the question to image and calculate the answer in the server.
Send the question image to the client.
The client sends the answer to the server.
"""


def make_question() -> tuple[Image.Image, int]:
    """
    To make a math question.
    :return: a tuple (Image, answer)
    """
    question = str(np.random.randint(0, 100))
    question += ' ' + np.random.choice(['+', '-']) + ' '
    question += str(np.random.randint(0, 100))
    question += ' ' + np.random.choice(['+', '-', '*']) + ' '
    question += str(np.random.randint(0, 100))
    answer = eval(question)
    question += ' = ?'
    img = Image.new('RGB', (100, 30), (255, 255, 255))
    img_draw = ImageDraw.Draw(img)
    img_draw.text((4, 9), question, fill=(np.random.randint(160, 230),
                                          np.random.randint(160, 230),
                                          np.random.randint(160, 230)))
    img_draw.text((6, 11), question, fill=(np.random.randint(0, 128),
                                           np.random.randint(0, 128),
                                           np.random.randint(0, 128)))
    return img, answer


def gen_page(uid: str) -> str:
    return render_template("human_check.html").replace('{client_uuid}', uid)
