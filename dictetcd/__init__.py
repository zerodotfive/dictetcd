import os
import etcd


class DictEtcd(dict):
    def __init__(self, prefix='/', etcd_client=etcd.Client(port=2379)):
        self.etcd_client = etcd_client
        self.prefix = prefix

    def __getitem__(self, key):
        path = os.path.join(self.prefix, str(key).replace('/', r'%252F'))
        try:
            result = self.etcd_client.get(path)
            if result.dir:
                return self.__class__(path, self.etcd_client)

            return result.value

        except etcd.EtcdKeyNotFound:
            raise KeyError

    def __setitem__(self, key, value):
        path = os.path.join(self.prefix, str(key).replace('/', r'%252F'))
        if isinstance(value, dict):
            try:
                result = self.etcd_client.get(path)
                if not result.dir:
                    del self[key]
                    raise etcd.EtcdKeyNotFound
            except etcd.EtcdKeyNotFound:
                self.etcd_client.write(path, None, None, True)

            for k, v in value.iteritems():
                tmp = self.__class__(path, self.etcd_client)
                tmp[k] = v

            return None

        if isinstance(value, list):
            try:
                result = self.etcd_client.get(path)
                if not result.dir:
                    del self[key]
                    raise etcd.EtcdKeyNotFound
            except etcd.EtcdKeyNotFound:
                self.etcd_client.write(path, None, None, True)

            for k in range(0, len(value)):
                    tmp = self.__class__(path, self.etcd_client)
                    tmp[str(k)] = value[k]

            return None

        try:
            result = self.etcd_client.get(path)
            if result.dir:
                raise etcd.EtcdNotFile
        except etcd.EtcdNotFile:
            del self[key]
        except etcd.EtcdKeyNotFound:
            pass
        self.etcd_client.set(path, value)

        return None

    def __delitem__(self, key):
        path = os.path.join(self.prefix, str(key).replace('/', r'%252F'))
        self.etcd_client.delete(path, True)

    def __iter__(self):
        tmp = self.etcd_client.get(self.prefix)
        for item in tmp._children:
            yield os.path.basename(item['key']).replace('%2F', r'/')

    def __str__(self):
        return "%s" % self.copy()

    def copy(self):
        tmp = dict()

        for key in self.iterkeys():
            if not isinstance(self[key], dict) and not isinstance(self[key], self.__class__):
                tmp[key] = self[key]
                continue

            path = os.path.join(self.prefix, str(key).replace('/', r'%252F'))
            tmp[key] = self.__class__(path, self.etcd_client).copy()

        return tmp

    def iterkeys(self):
        return self.__iter__()

    def iteritems(self):
        for key in self.__iter__():
            yield (key, self[key])

    def keys(self):
        tmp = list()
        for item in self.__iter__():
            tmp.append(item)

        return tmp

    def items(self):
        tmp = list()
        for item in self.iteritems():
            tmp.append(item)

        return tmp

    def itervalues(self):
        for key in self.__iter__():
            yield self[key]

    def values(self):
        tmp = list()
        for value in self.itervalues():
            tmp.append(value)

        return tmp
