import requests
from time import sleep
from libs.util import retry_timer as _retry_timer

def get_remote(url_inp):
    
    which_retry = 0

    while True and (which_retry < 10):
        
        try:
            resp = requests.get(url_inp)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            print('Failed to request from url {}, status code: {}. Retrying'.format(url_inp, resp.status_code), e )
            which_retry = which_retry + 1
            retry_sleep_time = _retry_timer( which_retry, 1, mode = 'multirand' ).get('interval')
            print('Retry ({}) in {} seconds.'.format(which_retry, retry_sleep_time))
            sleep(retry_sleep_time)
            pass


def dict_to_list(dic_inp, key_key_name = None, data_key_name = None):

    if key_index_name is None:
        key_index_name = 'index'
    
    if data_key_name is None:
        data_key_name = 'data'
    
    output = []
    if isinstance(dic_inp, dict ):
        for key, val in dic_inp.items():
            output.append(
                {
                    key_key_name: key,
                    data_key_name: val
                    }
            )

    return 
    
def clean_up_response(
    rsp_inp, 
    loaded_data = None, 
    list_data = True, 
    force_list_data = True
    ):
    
    # determine the data type
    if loaded_data is None:
        if list_data:
            loaded_data = []
        else:
            loaded_data = {}
    
    sol_keys = rsp_inp.get('sol_keys')

    current_data = {}
    if sol_keys is not None:
        for key in sol_keys:
            current_data[key] = rsp_inp.get(key)

    if isinstance(loaded_data, list):
        current_data = dict_to_list(current_data)
        loaded_data = loaded_data + current_data
    elif isinstance(loaded_data, dict):
        loaded_data = {**loaded_data, **current_data}

    if force_list_data and isinstance(loaded_data, dict):
        loaded_dta = dict_to_list(loaded_data)
    
    return loaded_data