using System;
class Check {
static object? consume_widget(object? _arg = null) => null;
    public static void Main() {
var item = (object?)null;
var my_data = (object?)null;
consume_widget(my_data);
my_data = item;
consume_widget(my_data);
    }
}
