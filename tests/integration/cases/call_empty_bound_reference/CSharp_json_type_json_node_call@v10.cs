using System.Text.Json.Nodes;
class Check {
static object? make_widget(object? value = null) => null;
    public static void Main() {
JsonNode? items = new JsonArray();
make_widget(((JsonNode?)items)?.DeepClone());
    }
}
