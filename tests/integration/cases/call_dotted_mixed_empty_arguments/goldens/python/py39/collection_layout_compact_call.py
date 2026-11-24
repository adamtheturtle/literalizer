from typing import Union
class _ThingType:
    def go(self, before: 'Union[tuple[object, ...], tuple[str, ...]]', populated: 'Union[tuple[int, ...], tuple[str, ...]]', after: 'Union[tuple[object, ...], tuple[int, ...]]') -> object: ...
thing = _ThingType()
thing.go(before=(), populated=(1,), after=())
thing.go(before=("text",), populated=(2,), after=())
thing.go(before=(), populated=("text",), after=())
thing.go(before=("text",), populated=(2,), after=(3,))
