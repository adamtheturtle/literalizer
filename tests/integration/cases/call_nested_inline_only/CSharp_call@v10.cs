using System;
class Check {
static object f(object a = null, object b = null) => null;
    public static void Main() {
f(2, "hello");  // trailing note
f(3, "world");  // another note
    }
}
