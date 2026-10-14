class Check {
static object? make_widget(object? count = null) => null;
    public static void Main() {
var my_data = (`__LINE__ > 0) ? make_widget(42) : make_widget(42); // trailing `marker
    _ = my_data;
    }
}
