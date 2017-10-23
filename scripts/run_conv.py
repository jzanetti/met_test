import argparse
import math
from met_test import conv_process, model_process, general_process
import os

OBS_FM_LIST = ['FM-12', 'FM-15']

def setup_parser():
    """read the command line arguments"""
    PARSER = argparse.ArgumentParser(description='verification')
    PARSER.add_argument('wrfdata', type=str, help="wrf data path")
    PARSER.add_argument('obsdata', type=str, help="obs data path")
    PARSER.add_argument('verify_field', type=str, help="verify field, e.g., surface_temperature, suface_dewpoint, surface_wind_spd/dir")
    PARSER.add_argument('model_name', type=str, help="model name")
    PARSER.add_argument('analysis_time', type=str, help="yyyymmddThh")
    PARSER.add_argument('valid_time', type=str, help="yyyymmddThh")
    PARSER.add_argument('output', type=str, help="output path")
    PARSER.add_argument('--influ_range', dest='influ_range', default=0.05,
                        help='if the difference for the locations of model and obs is bigger than this (degree), \
                        than the obs is discarded')

    return PARSER.parse_args(['test/nz8kmN-NCEP_02_17101818_001.00.grb',
                              'test/obs_gts_2017-10-18_18:00:00.3DVAR',
                              'suface_dewpoint',
                              'nz8kmN-NCEP-obsnudge',
                              '20171018T18', '20171018T19',
                              'test'])  
    
    return PARSER.parse_args()        


def main(args):
    """
    nearest_model_lat/lon/value: the model value at the location which the nearest one to the observation location
    """
    obs_data = conv_process.read_obs(args.obsdata, OBS_FM_LIST)
    obs_list = conv_process.produce_obs_list(obs_data)
    
    used_field = general_process.return_model_obs_fields(args.verify_field)
    
    model_latlon_arrays, model_lat, model_lon, model_data = model_process.get_model_data(used_field, args)
    all_index = general_process.do_kdtree(model_latlon_arrays, obs_list)
    
    used_obs_list = []
    used_model_list = []
    
    stats_out = 'stats_conv_{}_{}_from_{}_valid_at_{}'.format(args.model_name, args.verify_field, args.analysis_time, args.valid_time)
    file = open(os.path.join(args.output, stats_out), 'w')
    
    for i, index in enumerate(all_index):
        nearest_model_lat = model_latlon_arrays[index][0]
        nearest_model_lon = model_latlon_arrays[index][1]
        dis = math.sqrt((nearest_model_lat - obs_list[i][0])**2 + (nearest_model_lon - obs_list[i][1])**2) 
        if dis < args.influ_range:
            nearest_model_value = model_process.find_value_from_model(nearest_model_lat, nearest_model_lon, model_lat, model_lon, model_data)
            obs_value = obs_data[i][used_field['obs']]
            file.write('accepted obs: {}/{}({}); model: {}/{}({})\n'.format(obs_list[i][0], obs_list[i][1], obs_value, nearest_model_lat, nearest_model_lon, nearest_model_value)) 
            used_obs_list.append(obs_value)
            used_model_list.append(nearest_model_value)
        else:
            file.write('discarded obs: {}/{}; model: {}/{} (dis: {})\n'.format(obs_list[i][0], obs_list[i][1], nearest_model_lat, nearest_model_lon, dis))

    rmse, num_obs = general_process.cal_conv_skill(used_model_list, used_obs_list)
    print 'rmse = {}, n = {}'.format(rmse, num_obs)
    file.write('\n------------------------\n')
    file.write('rmse = {}, n = {}\n'.format(rmse, num_obs))
    file.close()
    
if __name__ == '__main__':
    args = setup_parser()
    main(args)
    
    
