using System.Text.Json.Nodes;
class Check {
static object? make_widget(object? before = null, object? populated = null, object? after = null) => null;
    public static void Main() {
make_widget(new JsonArray(), new JsonArray {1}, new JsonArray());
make_widget(new JsonArray {"text"}, new JsonArray {2}, new JsonArray());
make_widget(new JsonArray(), new JsonArray {"text"}, new JsonArray());
make_widget(new JsonArray {"text"}, new JsonArray {2}, new JsonArray {3});
    }
}
