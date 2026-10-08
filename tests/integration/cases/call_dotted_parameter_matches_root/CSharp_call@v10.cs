using System;
class Check {
class OuterType_ { public object inner(object outer = null, object n = null) => null; }
static OuterType_ outer = new OuterType_();
    public static void Main() {
outer.inner(1, 2);
    }
}
