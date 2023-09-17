import numpy as np
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw

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
    img = Image.new('RGB', (100, 30), (255, 255, 255))
    img_draw = ImageDraw.Draw(img)
    img_draw.text((10, 10), question, fill=(0, 0, 0))
    return img, answer

def gen_page(uid: str) -> str:

    page = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>
                Segment Anything in Remote Sensing Image
            </title>
        </head>
        <body>
            <img src="static/cache/{client_uuid}/question.png" alt="logo" width="100" height="100">
            <input type="text" id="answer" name="answer"/>
            <button onclick="submit()">Submit</button>
            <script>
                function submit() {
                    var answer = document.getElementById("answer").value;
                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", "/human_check", true);
                    xhr.setRequestHeader("Content-Type", "application/json");
                    xhr.send(JSON.stringify({uuid: "{client_uuid}", answer: answer}));
                    location.reload();
                }
            </script>
        </body>
        </html>
        """.replace('{client_uuid}', uid)
    return page
