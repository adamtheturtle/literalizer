class _ThingType:
    def go(self, value: 'tuple[object, ...]') -> object: ...
thing = _ThingType()
my_data = thing.go(value=())
