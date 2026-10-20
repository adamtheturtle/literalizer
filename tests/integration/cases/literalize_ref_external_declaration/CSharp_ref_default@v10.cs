using System;
class Check {
static object? consume_widget(object? arg_value = null) => null;
    public static void Main() {
var shared = (
    1,
    2
);
var my_data = shared;
consume_widget(my_data);
    }
}
