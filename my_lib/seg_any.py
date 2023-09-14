from typing import Optional
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
import numpy as np
from osgeo import gdal
from . import chpt

def segment(src_raster: str,
            out_raster: str,
            rgb_index: list = [1, 1, 1],
            points_per_side: Optional[int] = 64,
            points_per_batch: int = 64,
            pred_iou_thresh: float = 0.88,
            stability_score_thresh: float = 0.95,
            stability_score_offset: float = 1.0,
            box_nms_thresh: float = 0.7,
            crop_n_layers: int = 0,
            crop_nms_thresh: float = 0.7,
            crop_overlap_ratio: float = 512 / 1500,
            crop_n_points_downscale_factor: int = 1,
            min_mask_region_area: int = 100) -> None:
    '''
    :param src_raster: source raster path
    :param out_raster: output raster path (must be .tif)
    :param rgb_index: [r, g, b] index of bands, int in tuple, start from 1
    :param points_per_side: The number of points to be sampled along one side of the image. The total number of points is points_per_side**2. If None, 'point_grids' must provide explicit point sampling.
    :param points_per_batch:
    :param pred_iou_thresh:
    :param stability_score_thresh:
    :param stability_score_offset:
    :param box_nms_thresh:
    :param crop_n_layers:
    :param crop_nms_thresh:
    :param crop_overlap_ratio:
    :param crop_n_points_downscale_factor:
    :param min_mask_region_area:
    '''


    # load model
    sam = sam_model_registry['vit_h'](checkpoint=chpt)
    mask_generator = SamAutomaticMaskGenerator(sam,
                                               points_per_side=points_per_side,
                                               points_per_batch=points_per_batch,
                                               pred_iou_thresh=pred_iou_thresh,
                                               stability_score_thresh=stability_score_thresh,
                                               stability_score_offset=stability_score_offset,
                                               box_nms_thresh=box_nms_thresh,
                                               crop_n_layers=crop_n_layers,
                                               crop_nms_thresh=crop_nms_thresh,
                                               crop_overlap_ratio=crop_overlap_ratio,
                                               crop_n_points_downscale_factor=crop_n_points_downscale_factor,
                                               min_mask_region_area=min_mask_region_area)

    # load image
    raster = gdal.Open(src_raster)
    bands_mat = np.dstack((raster.GetRasterBand(rgb_index[0]).ReadAsArray(),
                           raster.GetRasterBand(rgb_index[1]).ReadAsArray(),
                           raster.GetRasterBand(rgb_index[2]).ReadAsArray()))
    geo_trans = raster.GetGeoTransform()

    # generate mask
    mask = mask_generator.generate(bands_mat)
    # write mask as raster
    matrix = sum(np.asarray(mask[i - 1]['segmentation'] * i, dtype=np.uint8) for i in range(1, len(mask) + 1))

    # export
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(out_raster, bands_mat.shape[1], bands_mat.shape[0], 1, gdal.GDT_Byte)
    dataset.SetGeoTransform(raster.GetGeoTransform())
    dataset.GetRasterBand(1).SetNoDataValue(-1)
    dataset.GetRasterBand(1).WriteArray(matrix)
    dataset.SetProjection(raster.GetProjection())
    dataset.FlushCache()

    # close
    raster = None
    dataset = None
