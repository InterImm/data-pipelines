import os
from libs.util import PersistentData as _PersistentData
from libs.util import retry_timer as _retry_timer
from libs.insight_weather import get_remote as _get_remote
from libs.insight_weather import clean_up_response as _clean_up_response

__location__ = os.path.realpath( os.path.join(os.getcwd(), os.path.dirname(__file__)))

data_file_path = os.path.join(__location__, 'data/insight-weather.json')

url_base = 'https://mars.nasa.gov/rss/api/?feed=weather&category=insight&feedtype=json&ver=1.0'

data = _PersistentData(data_file_path, format='json')

#get_remote(url_base)

data = _clean_up_response(_get_remote(url_base), loaded_data=data)

data.sync()