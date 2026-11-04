from typing import Union
class _ThingType:
    def go(self, before: 'Union[list[object], list[str]]', populated: 'Union[list[int], list[str]]', after: 'Union[list[object], list[int]]') -> object: ...
thing = _ThingType()
thing.go(before=[], populated=[1], after=[])
thing.go(before=["text"], populated=[2], after=[])
thing.go(before=[], populated=["text"], after=[])
thing.go(before=["text"], populated=[2], after=[3])
