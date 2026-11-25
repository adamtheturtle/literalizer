using System;
class Check {
static object? make_widget(object? count = null) => null;
    public static void Main() {
var my_data = make_widget(7) != null ?
make_widget(7) // inner
: null; // trailing
    _ = my_data;
    }
}
