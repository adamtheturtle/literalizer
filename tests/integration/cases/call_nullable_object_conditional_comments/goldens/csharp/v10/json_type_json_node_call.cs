using System.Text.Json.Nodes;
class Check {
static object? make_widget(object? count = null) => null;
    public static void Main() {
var my_data = make_widget((JsonNode?)(42)) != null ?
make_widget((JsonNode?)(42)) // inner
: null; // trailing
    _ = my_data;
    }
}
