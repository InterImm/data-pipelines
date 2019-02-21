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
    
def clean_up_response(rsp_inp, loaded_data = None):
    
    if loaded_data is None:
        loaded_data = {}
    
    sol_keys = rsp_inp.get('sol_keys')

    if sol_keys is not None:
        for key in sol_keys:
            loaded_data[key] = rsp_inp.get(key)
    
    return loaded_data