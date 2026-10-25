using System.Text.Json.Nodes;
class Check {
static object? consume_widget(object? arg_value = null) => null;
    public static void Main() {
JsonNode? item = (JsonNode?)null;
JsonNode? my_data = (JsonNode?)null;
consume_widget(((JsonNode?)my_data)?.DeepClone());
my_data = ((JsonNode?)item)?.DeepClone();
consume_widget(((JsonNode?)my_data)?.DeepClone());
    }
}
