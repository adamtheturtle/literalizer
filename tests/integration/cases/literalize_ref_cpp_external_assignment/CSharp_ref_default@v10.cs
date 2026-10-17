using System;
class Check {
static object? consume_widget(object? _arg = null) => null;
    public static void Main() {
var ref_data = (
    1,
    2
);
var my_data = ValueTuple.Create(
    0
);
consume_widget(my_data);
my_data = ref_data;
consume_widget(my_data);
    }
}
