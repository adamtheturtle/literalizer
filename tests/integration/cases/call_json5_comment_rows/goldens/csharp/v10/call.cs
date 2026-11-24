using System;
class Check {
static object? f(object? a = null, object? b = null) => null;
    public static void Main() {
// calls heading
// before call one
// first argument
f(1, 2);  // after call one
// second argument
f(3, 4);
// after all calls
    }
}
