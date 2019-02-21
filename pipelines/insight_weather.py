import os
from libs.util import PersistentData as _PersistentData
from libs.util import retry_timer as _retry_timer
from libs.insight_weather import get_remote as _get_remote
from libs.insight_weather import clean_up_response as _clean_up_response

__location__ = os.path.realpath( os.path.join(os.getcwd(), os.path.dirname(__file__)))

full_data_file_path = os.path.join(__location__, '../dapi/insight-weather/all.json')
recent_data_file_path = os.path.join(__location__,  '../dapi/insight-weather/recent.json')

url_base = 'https://mars.nasa.gov/rss/api/?feed=weather&category=insight&feedtype=json&ver=1.0'

recent_data_dict = _get_remote(url_base)

# 
recent_data = _PersistentData(recent_data_file_path, format='json')
recent_data.clear()
recent_data = _clean_up_response(recent_data_dict, loaded_data=recent_data )
recent_data.sync()

full_data = _PersistentData(full_data_file_path, format='json')
full_data = _clean_up_response(_get_remote(url_base), loaded_data=full_data)
full_data.sync()



records_data_file_path = os.path.join(
    __location__,  
    '../dapi/insight-weather/records/{}.json'
    .format(max([ int(key) for key in recent_data_dict.get('sol_keys') ])) 
    )
records_data = _PersistentData(records_data_file_path, format='json')
records_data = _clean_up_response(recent_data_dict, loaded_data=records_data )
records_data.sync()