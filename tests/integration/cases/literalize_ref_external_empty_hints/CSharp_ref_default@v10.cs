using System;
class Check {
static object? consume_widget(object? arg_value = null) => null;
    public static void Main() {
var item = (
    1,
    2
);
var my_data = (
    1,
    2
);
consume_widget(my_data);
my_data = item;
consume_widget(my_data);
    }
}
