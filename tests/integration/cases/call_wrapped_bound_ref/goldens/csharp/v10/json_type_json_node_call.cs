using System.Text.Json.Nodes;
class Check {
static object? make_widget(object? value = null) => null;
    public static void Main() {
JsonNode? value = (JsonNode?)(1);
make_widget(((JsonNode?)value)?.DeepClone());
    }
}
