using System.Text.Json.Nodes;
class Check {
static object? consume_widget(object? arg_value = null) => null;
    public static void Main() {
JsonNode? shared = new JsonArray {
    1,
    2
};
JsonNode? my_data = ((JsonNode?)shared)?.DeepClone();
consume_widget(((JsonNode?)my_data)?.DeepClone());
    }
}
