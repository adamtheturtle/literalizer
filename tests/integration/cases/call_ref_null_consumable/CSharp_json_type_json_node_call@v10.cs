using System.Text.Json.Nodes;
class Check {
static object? consume(object? value = null) => null;
    public static void Main() {
JsonNode? my_null = (JsonNode?)null;
JsonNode? regular_null = (JsonNode?)null;
consume(((JsonNode?)my_null)?.DeepClone());
consume(((JsonNode?)regular_null)?.DeepClone());
    }
}
