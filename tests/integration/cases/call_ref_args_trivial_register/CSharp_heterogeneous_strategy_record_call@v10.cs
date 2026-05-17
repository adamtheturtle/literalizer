using System;
using System.Collections.Generic;
class Check {
static object process(object value = null, object count = null) => null;
    public static void Main() {
var my_int = 1;
var my_bool = true;
var my_float = 3.14;
var my_list = new int[] {
    1,
    2,
    3
};
process(my_int, 42);
process(my_bool, 7);
process(my_float, 9);
process(my_list, 1);
    }
}
