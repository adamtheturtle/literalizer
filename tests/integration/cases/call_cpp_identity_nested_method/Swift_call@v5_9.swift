class _thingType { @discardableResult func go() -> Any { 0 } }
class _outerType { var thing = _thingType() }
let outer = _outerType()
outer.thing.go();
