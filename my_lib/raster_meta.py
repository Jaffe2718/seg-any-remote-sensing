from . import color_map
from osgeo import gdal
import numpy as np
import PIL.Image


def get_raster_meta(raster_path: str) -> dict:
    raster = gdal.Open(raster_path)
    if raster is None:
        raise Exception('cannot open raster')
    meta = {
        'width': raster.RasterXSize,
        'height': raster.RasterYSize,
        'X resolution': raster.GetGeoTransform()[1],
        'Y resolution': raster.GetGeoTransform()[5],
        'band_count': raster.RasterCount,
        'band_meta': []
    }
    for i in range(raster.RasterCount):
        band = raster.GetRasterBand(i + 1)
        meta['band_meta'].append({
            'description': band.GetDescription(),
            'min': band.GetMinimum(),
            'max': band.GetMaximum(),
            'nodata': band.GetNoDataValue(),
            'scale': band.GetScale(),
            'offset': band.GetOffset()
        })
    return meta


def gen_preview_raster_png(src_raster: str,
                           out_png: str,
                           rgb_index: list | tuple = (1, 1, 1)) -> None:
    """
    :param src_raster: absolute path of the source raster
    :param out_png: absolute path of the output PNG file
    :param rgb_index: index of RGB bands, int in tuple or list, start from 1
    """
    raster = gdal.Open(src_raster)
    # get color depth: 0-255 or 0-65535 or others
    depth = raster.GetRasterBand(1).DataType
    # get RGB bands
    bands_mat = np.dstack((raster.GetRasterBand(rgb_index[0]).ReadAsArray(),
                           raster.GetRasterBand(rgb_index[1]).ReadAsArray(),
                           raster.GetRasterBand(rgb_index[2]).ReadAsArray()))
    # remap to 0-255
    match depth:
        case gdal.GDT_Byte:
            pass
        case gdal.GDT_UInt16:
            bands_mat = (bands_mat / 65535 * 255).astype(np.uint8)
        case gdal.GDT_UInt32:
            bands_mat = (bands_mat / 4294967296 * 255).astype(np.uint8)
        case gdal.GDT_Int16:
            bands_mat = np.abs(bands_mat / 32768 * 255).astype(np.uint8)
        case gdal.GDT_Int32:
            bands_mat = np.abs(bands_mat / 2147483648 * 255).astype(np.uint8)
        case _:
            raise ValueError('unsupported color depth')
    # export
    img = PIL.Image.fromarray(bands_mat)
    img.save(out_png)


def gen_preview_mask_png(src_mask: str, out_png: str) -> None:
    """
    :param src_mask: absolute path of the source mask raster
    :param out_png: absolute path of the output PNG file
    """
    mask = gdal.Open(src_mask)
    matrix = mask.GetRasterBand(1).ReadAsArray()  # m * n * 1
    # get max value in the raster
    colors = color_map.gen_RGB_list(np.max(matrix) + 1)
    # remap to RGB: m * n * 3
    rgb = np.zeros(matrix.shape, dtype=np.uint8), np.zeros(matrix.shape, np.uint8), np.zeros(matrix.shape, np.uint8)
    for c in range(3):
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                rgb[c][i][j] = colors[matrix[i][j]][c]
    # export
    img = PIL.Image.fromarray(np.dstack(rgb))
    img.save(out_png)
