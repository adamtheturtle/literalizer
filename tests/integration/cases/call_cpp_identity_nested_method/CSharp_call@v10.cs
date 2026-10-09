using System;
class Check {
class ThingType_ { public object go() => null; }
class OuterType_ { public ThingType_ thing = new ThingType_(); }
static OuterType_ outer = new OuterType_();
    public static void Main() {
outer.thing.go();
    }
}
