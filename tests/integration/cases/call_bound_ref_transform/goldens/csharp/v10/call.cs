using System;
class Check {
static object? f(object? a = null) => null;
static object? repr(object? _arg = null) => null;
    public static void Main() {
var ref_data = 1;
repr(f(ref_data));
    }
}
