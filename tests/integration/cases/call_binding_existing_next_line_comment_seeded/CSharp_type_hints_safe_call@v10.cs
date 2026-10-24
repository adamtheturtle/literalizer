class Check {
static object? make_widget(object? count = null) => null;
static object? consume_widget(object? count = null) => null;
    public static void Main() {
var my_data = make_widget(42);
consume_widget(my_data);
my_data = make_widget(my_data);
// note
consume_widget(my_data);
    }
}
