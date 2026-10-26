using System;
class Check {
static object? make_widget(object? value = null) => null;
static object? consume(object? value = null) => null;
    public static void Main() {
var my_data = make_widget(42);
consume(my_data);
    }
}
