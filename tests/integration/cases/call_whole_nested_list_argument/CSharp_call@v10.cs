using System;
class Check {
static object f(object a = null) => null;
    public static void Main() {
f(((1, 2), ValueTuple.Create(3)));
    }
}
