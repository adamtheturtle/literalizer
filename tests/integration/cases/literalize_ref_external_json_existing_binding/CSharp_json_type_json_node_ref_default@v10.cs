using System.Text.Json.Nodes;
class Check {
static object? consume_widget(object? arg_value = null) => null;
    public static void Main() {
JsonNode? my_data = new JsonObject {
    ["a"] = 0
};
consume_widget(((JsonNode?)my_data)?.DeepClone());
my_data = new JsonObject {
    ["a"] = 1
};
consume_widget(((JsonNode?)my_data)?.DeepClone());
    }
}
