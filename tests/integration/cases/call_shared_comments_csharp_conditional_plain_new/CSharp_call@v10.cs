#nullable enable annotations
class Check {
static object make_widget(object count = null) => null;
    public static void Main() {
var my_data = ($"{(true ? "// payload" : "ok")}").Length >= 0 ? make_widget(42) : make_widget(42);
    _ = my_data;
    }
}
