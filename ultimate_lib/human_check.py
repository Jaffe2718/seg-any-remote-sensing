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
    page = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <link rel="icon" href="static/res/favicon.ico" type="image/x-icon"/>
            <title>
                Segment Anything in Remote Sensing Image
            </title>
        </head>
        <body>
            <h1 style="text-align: center">Human Check</h1>
            <div style="text-align: center; margin: 0 auto;">
                <img src="static/cache/{client_uuid}/question.png"
                 alt="check" style="width: 300px; height: 180px;"/>
                 <br>
                <input type="text" 
                       id="answer" name="answer" 
                       placeholder="Enter your answer here to pass the human check"
                       size="40"/>
                <br>
                <button onclick="submit()">Submit</button>
            </div>
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
