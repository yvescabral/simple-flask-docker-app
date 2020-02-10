import json
import os
import os.path as P


class RunningInstancesRepository:
    DATA_FILE_NAME = 'data.json'

    def __init__(self, fn=None):
        self.data_fn = fn or self.DATA_FILE_NAME
        self.init_data()

    def init_data(self):
        self.data = {}
        if P.isfile(self.data_fn):
            with open(self.data_fn) as data_fp:
                self.data = json.load(data_fp)

    def save(self):
        if P.isfile(self.data_fn):
            os.remove(self.data_fn)

        with open(self.data_fn, 'w') as data_fp:
            json.dump(self.data, data_fp)

    def set_instance(self, image_key, container_id, port_number):
        self.data[image_key] = {
            'container_id': container_id,
            'port_number': port_number
        }
        self.save()

    def get_instance(self, image_key):
        return self.data.get(image_key)

    def remove_instance(self, image_key):
        self.data.pop(image_key)
        self.save()

    def get_running_ports(self):
        return [v['port_number'] for v in self.data.values()]
