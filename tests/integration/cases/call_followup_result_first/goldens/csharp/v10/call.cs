using System;
class Check {
static object? make_widget(object? first = null, object? second = null) => null;
static object? consume(object? first = null, object? second = null) => null;
    public static void Main() {
var my_data = make_widget(42, 3);
consume(my_data, 3);
    }
}
