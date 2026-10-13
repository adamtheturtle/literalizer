class Check {
static object make_widget(object count = null) => null;
    public static void Main() {
var my_data = make_widget(42);
my_data = make_widget(my_data);
make_widget(my_data);
    }
}
