class OuterThing_ {
    construct new() {}
    go() {}
}
class Outer_ {
    thing { _thing }
    construct new() {
        _thing = OuterThing_.new()
    }
}
var outer = Outer_.new()
outer.thing.go()
