import os
import json
import requests
import time
import pickle, csv, shutil


class PersistentData(dict):
    ''' A dict that can be used to sync data between mem and disk.
    '''

    def __init__(self, filename, flag='c', mode=None, format='pickle', *args, **kwds):
        self.flag = flag                    # r=readonly, c=create, or n=new
        self.mode = mode                    # None or an octal triple like 0644
        self.format = format                # 'csv', 'json', or 'pickle'
        self.filename = filename
        if flag != 'n' and os.access(filename, os.R_OK):
            fileobj = open(filename, 'rb' if format == 'pickle' else 'r')
            with fileobj:
                self.load(fileobj)
        dict.__init__(self, *args, **kwds)

    def sync(self):
        '''
        Write the dictionary to disk
        '''
        if self.flag == 'r':
            return
        filename = self.filename
        tempname = filename + '.tmp'
        fileobj = open(tempname, 'wb' if self.format == 'pickle' else 'w')
        try:
            self.dump(fileobj)
        except Exception:
            os.remove(tempname)
            raise
        finally:
            fileobj.close()
        shutil.move(tempname, self.filename)    # atomic commit
        if self.mode is not None:
            os.chmod(self.filename, self.mode)

    def close(self):
        '''
        Write the dictionary to the corresponding file on disk
        '''
        self.sync()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()

    def dump(self, fileobj):
        if self.format == 'csv':
            csv.writer(fileobj).writerows(self.items())
        elif self.format == 'json':
            json.dump(self, fileobj, indent=2, separators=(',', ':'))
        elif self.format == 'pickle':
            pickle.dump(dict(self), fileobj, 2)
        else:
            raise NotImplementedError('Unknown format: ' + repr(self.format))

    def load(self, fileobj):
        # try formats from most restrictive to least restrictive
        for loader in (pickle.load, json.load, csv.reader):
            fileobj.seek(0)
            try:
                return self.update(loader(fileobj))
            except Exception:
                pass
        raise ValueError('File not in a supported format')


def retry_timer(which_retry, retry_base_interval, mode = None):
    """Calculate a random retry interval

    Args:
        mode(optional, default=None): specify the mode of retry time
            list of possible values: 'random', 'multiply', 'multirand'
    """

    if mode == None:
        mode = 'random'

    if mode == 'random':
        retry_wait_interval = retry_base_interval * random.random()
    elif mode == 'multiply':
        retry_wait_interval = which_retry * retry_base_interval
    elif mode == 'multirand':
        retry_wait_interval = which_retry * retry_base_interval * random.random()

    return {'mode': mode, 'interval': retry_wait_interval, 'retry': which_retry }