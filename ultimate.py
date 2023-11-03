__doc__ = """
In Ultimate version, the server will be able to handle multiple clients at the same time.

Modify the configuration.json to change the server configuration:
- host: the host ip of the server, 'auto' means auto detect the host
- port: the port of the server
- debug: whether to enable debug mode
- multi_thread: whether to enable multi-thread mode to handle multiple clients at the same time
- ip_access_limit: the limit of the IP access frequency, like:
    [
        "150/day",
        "25/hour",
        "10/minute",
        "1/second"
    ]
    means 150 times per day, 25 times per hour, 10 times per minute, 1 time per second.
    For more information, see https://flask-limiter.readthedocs.io/en/stable/configuration.html#ratelimit-string

To avoid DDOS attacks, the server adopts the following methods:
- Each client will be assigned a UUID, which will be stored in the cookie of the client.
- When a new client connects to the server, the server will check if the client has cookie and is human.
- The client info cookie will be expired after 7 days.
- If the client fails the human check, the server will increase the response delay time for the client.
- Limit IP access frequency: 150/day, 25/hour, 10/minute, 1/second

This program uses Flask to build the server. See https://flask.palletsprojects.com/

It uses Segment Anything | Meta AI Research Lab to segment the raster. See https://segment-anything.com/

Use Pillow to process the image. See https://pillow.readthedocs.io/en/stable/
    The Python Imaging Library (PIL) is
    
        Copyright © 1997-2011 by Secret Labs AB
        Copyright © 1995-2011 by Fredrik Lundh
    
    Pillow is the friendly PIL fork. It is
    
        Copyright © 2010-2023 by Jeffrey A. Clark (Alex) and contributors.

"""

import json
import os
import pathlib
import socket
import time
import uuid

from flask import Flask, request, abort, send_file, jsonify, make_response, send_from_directory, url_for, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from ultimate_lib import cleaner, raster_meta, seg_any, client_info, human_check

# load configuration.json
config: dict = json.load(open('configuration.json', 'r'))

app = Flask(__name__,
            static_folder=pathlib.Path(__file__).parent.absolute() / 'front_end',
            template_folder=pathlib.Path(__file__).parent.absolute() / 'templates')
limiter = Limiter(app=app, key_func=get_remote_address,                        # limit the access frequency
                  default_limits=config['ip_access_limit']) if len(config['ip_access_limit']) > 0 else None


app.config['client_info']: dict[str, client_info.ClientInfo] = {}                         # client info dict
app.config['cache_root'] = pathlib.Path(__file__).parent.absolute() / 'front_end' / 'cache'  # cache folder


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Check if the client has cookie, if not, create one.
    Show the index page. (Home page)
    :return: the index page
    """
    if 'uuid' not in request.cookies:  # new client
        # if the client has no cookie, create one
        c_uuid = str(uuid.uuid4())
        app.config['client_info'][c_uuid] = client_info.ClientInfo(c_uuid, time.time())
        res = make_response(human_check.gen_page(c_uuid))  # generate the page
        res.set_cookie('uuid', c_uuid)  # set cookie
        if not (app.config['cache_root'] / c_uuid).exists():
            (app.config['cache_root'] / c_uuid).mkdir()  # make cache folder for the client
        # human check here
        time.sleep(app.config['client_info'][c_uuid].force_delay)
        delay_increase(c_uuid)
        question_img, correct_answer = human_check.make_question()
        question_img.save(str(app.config['cache_root'] / c_uuid / 'question.png'))  # cache question image
        app.config['client_info'][c_uuid].answer = correct_answer  # store the answer
        return res
    else:  # if the client has cookie, check if the cookie is valid
        c_uuid = request.cookies.get('uuid')
        if c_uuid not in app.config['client_info'].keys():  # expired client
            # create a new client and reuse the uuid
            app.config['client_info'][c_uuid] = client_info.ClientInfo(c_uuid, time.time())
            if not (app.config['cache_root'] / c_uuid).exists():
                (app.config['cache_root'] / c_uuid).mkdir()  # make cache folder for the client
            res = make_response(human_check.gen_page(c_uuid))  # generate the page
            res.set_cookie('uuid', c_uuid)  # set cookie
            # human check here
            time.sleep(app.config['client_info'][c_uuid].force_delay)
            delay_increase(c_uuid)
            question_img, correct_answer = human_check.make_question()
            app.config['client_info'][c_uuid].answer = correct_answer
            question_img.save(str(app.config['cache_root'] / c_uuid / 'question.png'))  # cache question image
            return res
        else:  # valid client
            app.config['client_info'][c_uuid].connected_time = time.time()  # update the connected time
            if not app.config['client_info'][c_uuid].is_human:  # human check here
                time.sleep(app.config['client_info'][c_uuid].force_delay)
                delay_increase(c_uuid)
                res = make_response(human_check.gen_page(c_uuid))  # generate the page
                res.set_cookie('uuid', c_uuid)  # set cookie
                question_img, correct_answer = human_check.make_question()
                if not (app.config['cache_root'] / c_uuid).exists():
                    (app.config['cache_root'] / c_uuid).mkdir()
                question_img.save(str(app.config['cache_root'] / c_uuid / 'question.png'))
                app.config['client_info'][c_uuid].answer = correct_answer
                return res
            if app.config['client_info'][c_uuid].is_human:
                return redirect("front_end/quasar-project/dist/spa/index.html", code=302, Response=None)
            # //send_from_directory(app.template_folder, 'index.html'))


@app.route('/human_check', methods=['POST'])
def handle_human_check():
    """
    To check the human input.
    Receive the answer from the client as JSON. {"uuid": "xxx", "answer": answer}
    """
    time.sleep(app.config['client_info'][request.json['uuid']].force_delay)
    client_id = request.json['uuid']
    answer = int(request.json['answer'])
    if app.config['client_info'][client_id].answer == answer:
        app.config['client_info'][client_id].is_human = True
        app.config['client_info'][client_id].force_delay = 0.2    # reset the delay time
    elif not app.config['client_info'][client_id].is_human:
        delay_increase(client_id)  # increase the delay time to avoid DDOS
    return index()  # return the index page or human check page


def delay_increase(client_id: str):
    """
    Increase the delay time to avoid DDOS.
    :param client_id: the client id
    """
    global app
    if app.config['client_info'][client_id].force_delay < 1:
        app.config['client_info'][client_id].force_delay = 1
    elif app.config['client_info'][client_id].force_delay < 8:
        app.config['client_info'][client_id].force_delay += 1
    elif app.config['client_info'][client_id].force_delay < 1024:
        app.config['client_info'][client_id].force_delay *= 2
    else:
        app.config['client_info'][client_id].force_delay *= 1024


@app.route('/upload', methods=['POST'])
def handle_upload():
    """
    Uploads the raster file to the cache folder.
    :return: the message to show
    """
    time.sleep(app.config['client_info'][request.cookies.get('uuid')].force_delay)
    if not app.config['client_info'][request.cookies.get('uuid')].is_human:
        return abort(403, description='Invalid Client')
    for _file in (app.config['cache_root'] / request.cookies.get('uuid')).glob('*'):  # remove all cached files
        _file.unlink()
    app.config['client_info'][request.cookies.get('uuid')].cached_raster = ''
    app.config['client_info'][request.cookies.get('uuid')].cached_mask_raster = ''
    app.config['client_info'][request.cookies.get('uuid')].preview_raster_png = ''
    app.config['client_info'][request.cookies.get('uuid')].preview_mask_png = ''
    if request.files:
        for key in request.files.keys():
            raster_file = request.files[key]
            if raster_file.filename == '':
                return abort(400, description='no file selected')
            else:
                raster_file.save(str(app.config['cache_root'] / request.cookies.get('uuid') / raster_file.filename))
                app.config['client_info'][request.cookies.get('uuid')].cached_raster = raster_file.filename
        return 'Upload raster successfully!', 200
    else:
        return dir(request), 400


@app.route('/upload_cfg', methods=['POST'])
def handle_upload_cfg():
    """
    Uploads the configuration file of raster, like .tfw, .aux.xml, .prj, etc.
    :return: the message to show
    """
    time.sleep(app.config['client_info'][request.cookies.get('uuid')].force_delay)
    if not app.config['client_info'][request.cookies.get('uuid')].is_human:
        return abort(403, description='Invalid Client')
    if request.files:
        for key in request.files.keys():
            cfg_file = request.files[key]
            if cfg_file.filename == '':
                pass
            else:
                cfg_file.save(str(app.config['cache_root'] / request.cookies.get('uuid') / cfg_file.filename))
        return 'Upload raster configuration file successfully!', 200


@app.route('/raster_meta', methods=['GET'])
def handle_raster_meta():
    """
    Returns the metadata of the raster file.

    Receives the raster file name (not the full path) as a STRING.
    """
    time.sleep(app.config['client_info'][request.cookies.get('uuid')].force_delay)
    if not app.config['client_info'][request.cookies.get('uuid')].is_human:
        return abort(403, description='Invalid Client')
    raster_pth = (app.config['cache_root'] /
                  request.cookies.get('uuid') /
                  app.config['client_info'][request.cookies.get('uuid')].cached_raster)
    if raster_pth.exists() and raster_pth.is_file():
        return jsonify(
            raster_meta.get_raster_meta(
                str(app.config['cache_root'] /
                    request.cookies.get('uuid') /
                    app.config['client_info'][request.cookies.get('uuid')].cached_raster)))
    else:
        return abort(400, description='no raster file')


@app.route('/preview_raster', methods=['POST'])
def handle_preview_raster():
    """
    Returns the preview image of the raster file.

    Receives band indexes (begin from 1) as a JSON like {"r": 3, "g": 2, "b": 1}.
    """
    time.sleep(app.config['client_info'][request.cookies.get('uuid')].force_delay)
    if not app.config['client_info'][request.cookies.get('uuid')].is_human:
        return abort(403, description='Invalid Client')
    raster_pth = (app.config['cache_root'] / request.cookies.get('uuid') /
                  app.config['client_info'][request.cookies.get('uuid')].cached_raster)
    if raster_pth.exists() and raster_pth.is_file() and request.json:
        try:
            data = request.json
            app.config['client_info'][request.cookies.get('uuid')].preview_raster_png = \
                app.config['client_info'][request.cookies.get('uuid')].cached_raster + '.pre.png'
            raster_meta.gen_preview_raster_png(
                src_raster=str(app.config['cache_root'] / request.cookies.get('uuid') /
                               app.config['client_info'][request.cookies.get('uuid')].cached_raster),
                out_png=str(app.config['cache_root'] / request.cookies.get('uuid') /
                            app.config['client_info'][request.cookies.get('uuid')].preview_raster_png),
                rgb_index=(data['b'], data['g'], data['r'])
            )
            return send_file(str(app.config['cache_root'] / request.cookies.get('uuid') /
                                 app.config['client_info'][request.cookies.get('uuid')].preview_raster_png))
        except Exception as e:
            app.config['client_info'][request.cookies.get('uuid')].preview_raster_png = ''
            return abort(400, description=str(e))


@app.route('/segment', methods=['POST'])
def handle_segment():
    """
    Segments the image and returns the segmentation GeoTiff.

    * Use the uploaded raster file as the source raster.

    * This method is will create 1 cached file: the segmentation mask raster (GeoTiff)

    * Receives a JSON object with the following fields:
    - out_raster: name of the output raster file (GeoTiff), in the cache folder, must end with '.tif'
    - rgb_index: index of the RGB bands (begin from 1) in the source raster file, json array like [3, 2, 1]
    - points_per_side: number of points per side of the square (integer)
    - points_per_batch: number of points per batch (integer)
    - pred_iou_thresh: threshold of the predicted IoU (float)
    - stability_score_thresh: threshold of the stability score (float)
    - stability_score_offset: offset of the stability score (float)
    - box_nms_thresh: threshold of the box NMS (float)
    - crop_n_layers: number of layers of the crop (integer)
    - crop_nms_thresh: threshold of the crop NMS (float)
    - crop_overlap_ratio: overlap ratio of the crop (float)
    - crop_n_points_downscale_factor: downscale factor of the crop (integer)
    - min_mask_region_area: minimum area of the mask region (integer)
    """
    time.sleep(app.config['client_info'][request.cookies.get('uuid')].force_delay)
    if not app.config['client_info'][request.cookies.get('uuid')].is_human:
        return abort(403, description='Invalid Client')
    if request.json:
        # remove the old cached mask raster
        cached_mask_raster = app.config['cache_root'] / request.cookies.get('uuid') / \
                             app.config['client_info'][request.cookies.get('uuid')].cached_mask_raster
        if cached_mask_raster.exists() and cached_mask_raster.is_file():
            cached_mask_raster.unlink()
        # segment the raster and store the result in the cache folder
        try:
            data = request.json
            # segment the raster and store the result in the cache folder
            seg_any.segment(
                src_raster=str(app.config['cache_root'] / request.cookies.get('uuid') /
                               app.config['client_info'][request.cookies.get('uuid')].cached_raster),
                out_raster=str(app.config['cache_root'] / request.cookies.get('uuid') / data['out_raster']),
                rgb_index=data['rgb_index'],
                points_per_side=data['points_per_side'],
                points_per_batch=data['points_per_batch'],
                pred_iou_thresh=data['pred_iou_thresh'],
                stability_score_thresh=data['stability_score_thresh'],
                stability_score_offset=data['stability_score_offset'],
                box_nms_thresh=data['box_nms_thresh'],
                crop_n_layers=data['crop_n_layers'],
                crop_nms_thresh=data['crop_nms_thresh'],
                crop_overlap_ratio=data['crop_overlap_ratio'],
                crop_n_points_downscale_factor=data['crop_n_points_downscale_factor'],
                min_mask_region_area=data['min_mask_region_area'])
            app.config['client_info'][request.cookies.get('uuid')].cached_mask_raster = data['out_raster']
            return 'Segmentation finished successfully!', 200
        except Exception as e:
            print(e)
            app.config['client_info'][request.cookies.get('uuid')].cached_mask_raster = ''
            return abort(400, description='invalid data:' + e.__str__())


@app.route('/preview_mask', methods=['GET'])
def handle_preview_mask():
    """
    Generates the preview png of the segmentation mask and returns the preview png.
    """
    time.sleep(app.config['client_info'][request.cookies.get('uuid')].force_delay)
    if not app.config['client_info'][request.cookies.get('uuid')].is_human:
        return abort(403, description='Invalid Client')
    cached_mask_raster = app.config['cache_root'] / request.cookies.get('uuid') / \
                         app.config['client_info'][request.cookies.get('uuid')].cached_mask_raster
    if cached_mask_raster.exists() and cached_mask_raster.is_file():
        app.config['client_info'][request.cookies.get('uuid')].preview_mask_png = \
            app.config['client_info'][request.cookies.get('uuid')].cached_mask_raster + '.mask.png'
        raster_meta.gen_preview_mask_png(
            src_mask=str(app.config['cache_root'] / request.cookies.get('uuid') /
                         app.config['client_info'][request.cookies.get('uuid')].cached_mask_raster),
            out_png=str(app.config['cache_root'] / request.cookies.get('uuid') /
                        app.config['client_info'][request.cookies.get('uuid')].preview_mask_png))
        return send_file(str(app.config['cache_root'] / request.cookies.get('uuid') /
                             app.config['client_info'][request.cookies.get('uuid')].preview_mask_png), as_attachment=False)
    else:
        return abort(404, description='no segmentation mask raster found')


@app.route('/download', methods=['GET'])
def handle_download():
    """
    Downloads the segmentation mask raster.
    :return: the segmentation mask raster, as a GeoTiff file, call the client browser to download it
    """
    time.sleep(app.config['client_info'][request.cookies.get('uuid')].force_delay)
    if not app.config['client_info'][request.cookies.get('uuid')].is_human:
        return abort(403, description='Invalid Client')
    mask_pth = app.config['cache_root'] / request.cookies.get('uuid') / \
               app.config['client_info'][request.cookies.get('uuid')].cached_mask_raster
    if mask_pth.exists() and mask_pth.is_file():
        return send_file(str(app.config['cache_root'] / request.cookies.get('uuid') /
                             app.config['client_info'][request.cookies.get('uuid')].cached_mask_raster), as_attachment=True)
    else:
        return abort(404, description='no segmentation mask raster found')


if __name__ == '__main__':
    print(__doc__)
    for root, dirs, files in os.walk(str(app.config['cache_root'])):  # clean the cache folder first
        for file in files:
            os.remove(os.path.join(root, file))
    for root, dirs, files in os.walk(str(app.config['cache_root'])):
        for dir_ in dirs:
            os.rmdir(os.path.join(root, dir_))

    cleaner_thread = cleaner.CleanerThread(str(app.config['cache_root']))  # start the cleaner thread
    cleaner_thread.start()
    clean_client_thread = cleaner.CleanClientThread(app.config['client_info'])  # start the clean client thread
    clean_client_thread.start()
    # start the server
    app.run(host=socket.gethostbyname(socket.gethostname()) if config['host'] == 'auto' else config['host'],
            port=config['port'],
            debug=config['debug'],
            threaded=config['multi_thread'])
