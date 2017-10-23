import numpy
import pygrib
import sys
from metpy import calc
from metpy.units import units

def read_grib(wrfpath, wrf_field):
    """read data from a grib file"""
    grbs=pygrib.open(wrfpath)
    
    found_var = False
    for grb in grbs.select():
        if grb['name'] == wrf_field:
            found_var = True
            gg = grb
            break
    
    if found_var:
        print 'read model as: {}'.format(gg)
    else:
        sys.exit("Cannot find the field of {}".format(wrf_field))
        
    latlon = gg.latlons()
    model_lat = latlon[0]
    model_lon = latlon[1]
    model_lon[model_lon < 0.0]+=360.0
    
    model_data=gg.values
    model_latlon_arrays = numpy.dstack([model_lat.ravel(),model_lon.ravel()])[0]
    
    return model_latlon_arrays, model_lat, model_lon, model_data

def find_value_from_model(nearest_model_lat, nearest_model_lon, 
                          model_lat, model_lon,
                          model_data):
    
    """find the index of lat/lon in 2d arrays according to the given lat/lons
       inputs: nearest_model_lat/nearest_model_lon: the lat/lon of model the has the shortest distance to the obs
               model_lat/model_lon/model_data: 2d array from the grib file
       outputs: the model value at (nearest_model_lat, nearest_model_lon)
    """
    model_value = None
    lat_index = numpy.where(model_lat==nearest_model_lat)
    lon_index = numpy.where(model_lon==nearest_model_lon)
    if lat_index == lon_index:
        model_value = model_data[lat_index[0][0],lat_index[1][0]]
    return model_value

def get_model_data(used_field, args):
    """return model data according to the field to be verified"""
    if used_field['method'] == None:
        model_latlon_arrays, model_lat, model_lon, model_data = read_grib(args.wrfdata, used_field['model'])
    elif used_field['method'] == 'uv2spd' or used_field['method'] == 'uv2dir' :
        _, _, _, model_u_data = read_grib(args.wrfdata, used_field['model'][0])
        model_latlon_arrays, model_lat, model_lon, model_v_data = read_grib(args.wrfdata, used_field['model'][1])
        if used_field['method'] == 'uv2spd':
            model_u_data = model_u_data * (units.meters / units.second)
            model_v_data = model_v_data * (units.meters / units.second)
            model_data = (calc.get_wind_speed(model_u_data, model_v_data)).magnitude
        else:
            model_u_data = model_u_data * (units.meters / units.second)
            model_v_data = model_v_data * (units.meters / units.second)
            model_data = (calc.get_wind_dir(model_u_data, model_v_data)).magnitude
    
    return model_latlon_arrays, model_lat, model_lon, model_data

