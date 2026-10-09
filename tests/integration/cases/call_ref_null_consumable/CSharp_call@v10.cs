using System;
class Check {
static object consume(object value = null) => null;
    public static void Main() {
var my_null = (object?)null;
var regular_null = (object?)null;
consume(my_null);
consume(regular_null);
    }
}
