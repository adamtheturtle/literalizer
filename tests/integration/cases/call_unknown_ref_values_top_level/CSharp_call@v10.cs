using System;
class Check {
static object process(object data = null) => null;
    public static void Main() {
var known_value = 1;
var unknown_value = ValueTuple.Create();
process(unknown_value);
    }
}
