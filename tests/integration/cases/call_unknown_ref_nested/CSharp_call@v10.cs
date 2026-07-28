using System;
class Check {
static object process(object known_value = null, object nested_missing = null) => null;
    public static void Main() {
var known_value = true;
var unknown_value = true;
process(known_value, unknown_value);
    }
}
