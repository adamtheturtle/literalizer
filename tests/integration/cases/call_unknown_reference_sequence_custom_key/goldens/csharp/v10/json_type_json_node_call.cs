using System.Text.Json.Nodes;
class Check {
static object? process(object? data = null) => null;
    public static void Main() {
JsonNode? UntypedValue = new JsonArray();
process(new JsonArray {((JsonNode?)UntypedValue)?.DeepClone(), ((JsonNode?)UntypedValue)?.DeepClone()});
    }
}
