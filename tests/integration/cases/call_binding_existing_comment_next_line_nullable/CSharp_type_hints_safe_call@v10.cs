class Check {
static object? make_widget(object? count = null) => null;
static object? consume(object? count = null) => null;
    public static void Main() {
var my_data = make_widget((object?)null);
consume(my_data);
my_data = make_widget(42);
// note
consume(my_data);
    }
}
