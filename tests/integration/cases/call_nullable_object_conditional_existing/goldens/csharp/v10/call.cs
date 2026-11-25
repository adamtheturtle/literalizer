class Check {
static object? make_widget(object? count = null) => null;
static object? consume(object? count = null) => null;
    public static void Main() {
var my_data = make_widget(7);
consume(my_data);
my_data = make_widget(13) != null ?
make_widget(13) // inner
: null; // trailing
consume(my_data);
    }
}
