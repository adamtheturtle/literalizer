class _ThingType { def go(Map _args) { null } }
class _OuterType { def thing = new _ThingType() }
def outer = new _OuterType()
outer.thing.go()
