import math
from scipy import spatial
import numpy

def return_model_obs_fields(verif_field):
    if verif_field == 'surface_temperature':
        used_field = {'model': '2 metre temperature', 
                      'obs': 'surface_temperature',
                      'method': None}
    elif verif_field == 'suface_dewpoint':
        used_field = {'model': '2 metre dewpoint temperature', 
                      'obs': 'surface_dew_point',
                      'method': None}
    elif verif_field == 'surface_wind_spd':
        used_field = {'model': ['10 metre U wind component', '10 metre V wind component'],
                      'obs': 'surface_wind_spd',
                      'method': 'uv2spd'}
    elif verif_field == 'surface_wind_dir':
        used_field = {'model': ['10 metre U wind component', '10 metre V wind component'],
                      'obs': 'surface_wind_dir',
                      'method': 'uv2dir'}
    else:
        sys.exit("field {} is not supported".format(verif_field))
    
    return used_field       
    

def cal_conv_skill(model_data, obs_data):
    n = len(model_data)
    rmse = math.sqrt(sum((numpy.asarray(model_data) - numpy.asarray(obs_data))**2)/n)
    return rmse, n

def do_kdtree(combined_x_y_arrays,points):
    mytree = spatial.cKDTree(combined_x_y_arrays)
    dist, indexes = mytree.query(points)
    return indexes
