using System.Text.Json.Nodes;
class Check {
static object? process(object? data = null) => null;
    public static void Main() {
JsonNode? unknown_value = new JsonArray();
process(new JsonArray {((JsonNode?)unknown_value)?.DeepClone()});
    }
}
