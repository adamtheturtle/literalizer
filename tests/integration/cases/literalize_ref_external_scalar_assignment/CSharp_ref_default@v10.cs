using System;
class Check {
static object? consume_widget(object? arg_value = null) => null;
    public static void Main() {
var my_data = 0;
var shared = 1;
my_data = shared;
consume_widget(my_data);
    }
}
