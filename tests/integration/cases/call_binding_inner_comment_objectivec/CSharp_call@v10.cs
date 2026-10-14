class Check {
static object? make_widget(object? count = null) => null;
    public static void Main() {
var my_data = make_widget(42) ?
make_widget(42) // inner
: nil; // trailing
    _ = my_data;
    }
}
