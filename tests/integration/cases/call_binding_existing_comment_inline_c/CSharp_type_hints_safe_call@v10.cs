class Check {
static object? make_widget(object? count = null) => null;
    public static void Main() {
var my_data = make_widget(42);
make_widget(my_data);
my_data = make_widget(my_data); // note
make_widget(my_data);
    }
}
