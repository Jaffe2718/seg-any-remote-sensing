import webbrowser, pathlib
from flask import Flask, render_template, request, abort
from my_lib import port, seg_any

app = Flask(__name__,
            static_folder=pathlib.Path(__file__).parent.absolute() / 'static',
            template_folder=pathlib.Path(__file__).parent.absolute() / 'templates')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def handle_data():
    if request.data:
        raw_ = request.data.decode('utf-8')
        print(raw_)
        try:
            data = eval(raw_)
            seg_any.segment(src_raster=data['src_raster'],
                            out_raster=data['out_raster'],
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
            return 'ok'
        except Exception as e:
            print(e)
            return abort(400, description='invalid data:' + e.__str__())


if __name__ == '__main__':
    # get random port
    port = port.get_available_port()
    webbrowser.open('http://localhost:' + str(port))
    app.run(host='localhost', port=port)
