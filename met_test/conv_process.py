import struct

def produce_obs_list(obs_data):
    """write obs latlon into turple, e.g., [(lat1, lon1), (lat2, lon2), ...]"""
    obs_latlon = []
    for obs in obs_data:
        obs_latlon.append((obs['obs_lat'], obs['obs_lon']))
    return obs_latlon

def read_obs(obspath, obs_fm_list):
    """read obs information from the output of OBSPROC
       input: obspath: conv obs input path
              obs_fm_list: a list including the fm_code to be processed
       output: a list including all obs information
    """
    fobs = open(obspath, "r")
    next_sec = None
    read_on = False
    obs_data = [] # format: [obs_line1, obs_line2, ...]
    obs_line = {} # format: a turple include obs information
    for line in fobs:
        if line.startswith('FM-'):
            # read info
            (obs_fm, obs_datetime, obs_name, obs_lvl, obs_lat, obs_lon, obs_ele, obs_id) = struct.unpack("12sx19sx40sx6s12s11x12s11x12s11x6x40sx", line)
            if (obs_fm.strip()[0:5] in obs_fm_list) == False:
                read_on = False
                continue
            next_sec = 'srfc'
            read_on = True
            if len(obs_line) > 0:
                obs_data.append(obs_line)
            obs_line = []
            obs_line = {'obs_fm': obs_fm.strip()}
            obs_line.update({'obs_datetime': obs_datetime.strip()})
            obs_line.update({'obs_lat': float(obs_lat)})
            obs_line.update({'obs_lon': float(obs_lon)})
            obs_line.update({'obs_ele': float(obs_ele)})
            obs_line.update({'obs_id': obs_id.strip()})
            continue

        if next_sec == 'srfc' and read_on:
            # read srfc
            (slp, slp_qc, slp_err, pw, pw_qc, pw_err) = struct.unpack("12s4s7s12s4s7s", line[0:-1])
            next_sec = 'each'
            continue
        
        if next_sec == 'each' and read_on:
            (pres, pres_qc, pres_err, 
             spd, spd_qc, spd_err,
             dir, dir_qc, dir_err,
             hgt, hgt_qc, hgt_err,
             tmp, tmp_qc, tmp_err,
             dewp, dewp_qc, dewp_err,
             humid, humid_qc, humid_err) = struct.unpack("12s4s7s12s4s7s12s4s7s11x \
                                                          12s4s7s12s4s7s12s4s7s11x \
                                                          12s4s7s", line[0:-1])
            next_sec = 'each'
            obs_line.update({'surface_wind_spd': float(spd)})
            obs_line.update({'surface_wind_dir': float(dir)})
            obs_line.update({'surface_height': float(hgt)})
            obs_line.update({'surface_temperature': float(tmp)})
            obs_line.update({'surface_dew_point': float(dewp)})
            continue
    
    if len(obs_line) > 0:
        obs_data.append(obs_line)

    return obs_data
