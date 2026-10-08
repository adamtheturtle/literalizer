using System;
class Check {
static object f(object a = null) => null;
    public static void Main() {
f(ValueTuple.Create(1));  // note
    }
}
