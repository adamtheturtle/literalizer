using System;
class Check {
static object f(object ops = null) => null;
    public static void Main() {
f((("DEL", "b", "10"), ("ADD", "a", "x")));  // note
// next call
f(ValueTuple.Create(("ADD", "c", "y")));
    }
}
