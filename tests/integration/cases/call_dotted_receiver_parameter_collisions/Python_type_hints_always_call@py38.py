class _WorkerType:
    def process(_self, self: 'dict[object, object]', self_: 'dict[object, object]') -> object: ...
class _ApiType:
    worker = _WorkerType()
api = _ApiType()
api.worker.process(self={}, self_={})
