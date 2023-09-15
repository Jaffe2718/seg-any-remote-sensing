import pathlib
import webbrowser

from flask import Flask, render_template, request, abort, send_file, jsonify

from my_lib import cleaner, port, raster_meta, seg_any

app = Flask(__name__,
            static_folder=pathlib.Path(__file__).parent.absolute() / 'static',
            template_folder=pathlib.Path(__file__).parent.absolute() / 'templates')
app.config['cache_path'] = pathlib.Path(__file__).parent.absolute() / 'static' / 'cache'
app.config['cache_src_raster'] = ''    # no cached source raster initially
app.config['cache_mask_raster'] = ''   # no cached mask raster initially
app.config['preview_raster_png'] = ''  # no preview image initially
app.config['preview_mask_png'] = ''    # no preview image initially


@app.route('/', methods=['GET'])
def index():
    """
    Show the index page. (Home page)
    :return: the index page
    """
    for file in app.config['cache_path'].glob('*'):
        file.unlink()
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def handle_upload():
    """
    Uploads the raster file to the cache folder.
    :return: 'ok' if the upload is successful
    """
    for file in app.config['cache_path'].glob('*'):  # remove all cached files
        file.unlink()
    if request.files:
        file = request.files['file']
        if file.filename == '':
            return abort(400, description='no file selected')
        else:
            file.save(str(app.config['cache_path'] / file.filename))
            app.config['cache_src_raster'] = file.filename
            return 'Upload raster successfully!'


@app.route('/upload_cfg', methods=['POST'])
def handle_upload_cfg():
    """
    Uploads the configuration file of raster, like .tfw, .aux.xml, .prj, etc.
    :return: 'ok' if the upload is successful
    """
    if request.files:
        file = request.files['file']
        if file.filename == '':
            return abort(400, description='no file selected')
        else:
            file.save(str(app.config['cache_path'] / file.filename))
            return 'Upload raster configuration file successfully!'


@app.route('/raster_meta', methods=['GET'])
def handle_raster_meta():
    """
    Returns the metadata of the raster file.

    Receives the raster file name (not the full path) as a STRING.
    """
    raster_pth = app.config['cache_path'] / app.config['cache_src_raster']
    if raster_pth.exists() and raster_pth.is_file():
        return jsonify(raster_meta.get_raster_meta(str(app.config['cache_path'] / app.config['cache_src_raster'])))
    else:
        return abort(404, description='no raster file found')


@app.route('/preview_raster', methods=['POST'])
def handle_preview_raster():
    """
    Returns the preview image of the raster file.

    Receives band indexes (begin from 1) as a JSON like {"r": 3, "g": 2, "b": 1}.
    """
    raster_pth = app.config['cache_path'] / app.config['cache_src_raster']
    if raster_pth.exists() and raster_pth.is_file():
        if request.json:
            try:
                data = request.json
                app.config['preview_raster_png'] = app.config['cache_src_raster'] + '.pre.png'
                raster_meta.gen_preview_raster_png(
                    src_raster=str(app.config['cache_path'] / app.config['cache_src_raster']),
                    out_png=str(app.config['cache_path'] / app.config['preview_raster_png']),
                    rgb_index=(data['b'], data['g'], data['r']))
                return send_file(str(app.config['cache_path'] / app.config['preview_raster_png']), as_attachment=False)
            except Exception as e:
                print(e)
                app.config['preview_raster_png'] = ''
                return abort(400, description='invalid data:' + e.__str__())


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
    if request.json:
        # remove the old cached mask raster
        cached_mask_raster = app.config['cache_path'] / app.config['cache_mask_raster']
        if cached_mask_raster.exists() and cached_mask_raster.is_file():
            cached_mask_raster.unlink()
        # segment the raster and store the result in the cache folder
        try:
            data = request.json
            # segment the raster and store the result in the cache folder
            seg_any.segment(src_raster=str(app.config['cache_path'] /
                                           app.config['cache_src_raster']),  # use cached source raster
                            out_raster=str(app.config['cache_path'] / data['out_raster']),
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
            app.config['cache_mask_raster'] = data['out_raster']  # update cached mask raster name
            return 'Segmentation finished successfully!'
        except Exception as e:
            print(e)
            for file in app.config['cache_path'].glob('*'):
                file.unlink()
            return abort(400, description='invalid data:' + e.__str__())


@app.route('/preview_mask', methods=['GET'])
def handle_preview_mask():
    """
    Generates the preview png of the segmentation mask and returns the preview png.
    """
    cached_mask_raster = app.config['cache_path'] / app.config['cache_mask_raster']
    if cached_mask_raster.exists() and cached_mask_raster.is_file():
        app.config['preview_mask_png'] = app.config['cache_mask_raster'] + '.mask.png'
        raster_meta.gen_preview_mask_png(src_mask=str(app.config['cache_path'] / app.config['cache_mask_raster']),
                                         out_png=str(app.config['cache_path'] / app.config['preview_mask_png']))
        return send_file(str(app.config['cache_path'] / app.config['preview_mask_png']), as_attachment=False)
    else:
        return abort(404, description='no segmentation mask raster found')


@app.route('/download', methods=['GET'])
def handle_download():
    """
    Downloads the segmentation mask raster.
    :return: the segmentation mask raster, as a GeoTiff file, call the client browser to download it
    """
    mask_pth = app.config['cache_path'] / app.config['cache_mask_raster']
    if mask_pth.exists() and mask_pth.is_file():
        return send_file(str(app.config['cache_path'] / app.config['cache_mask_raster']), as_attachment=True)
    else:
        return abort(404, description='no segmentation mask raster found')


if __name__ == '__main__':
    t_clean = cleaner.CleanerThread(path=str(app.config['cache_path']))
    t_clean.start()
    # get random port
    port = port.get_available_port()
    webbrowser.open('http://localhost:' + str(port))
    app.run(host='localhost', port=port)
