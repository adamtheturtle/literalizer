from typing import Union
class _WorkerType:
    def process(self, values: 'Union[tuple[Union[int, dict[object, object]], ...], tuple[Union[int, dict[str, str]], ...]]', count: 'int') -> object: ...
class _ApiType:
    worker = _WorkerType()
api = _ApiType()
api.worker.process(values=(1, {}), count=42)
api.worker.process(values=(2, {"x": "s"}), count=43)
