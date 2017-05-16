**Class allows to work with etcd as with dict().**

Unfortunately, list() will be converted into dict on write.
To set key with TTL use tuple:

`dict_etcd['key'] = ('value', ttl_in_seconds)
`
