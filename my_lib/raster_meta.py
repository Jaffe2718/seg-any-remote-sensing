from osgeo import gdal
import json

def get_raster_meta(raster_path) -> str:
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
    return json.dumps(meta)