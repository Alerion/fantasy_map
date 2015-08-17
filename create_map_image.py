import gdal
import mapnik

stylesheet = 'world_style.xml'
hillshade = 'map.tif'


def main():
    raster = gdal.Open(hillshade)
    map_obj = mapnik.Map(raster.RasterXSize, raster.RasterYSize)  # EPSG:4326
    mapnik.load_map(map_obj, stylesheet)
    map_obj.zoom_all()
    mapnik.render_to_file(map_obj, 'world.png', 'png')


if __name__ == '__main__':
    main()
