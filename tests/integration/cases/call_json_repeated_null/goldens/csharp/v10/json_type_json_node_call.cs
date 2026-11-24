using System.Text.Json.Nodes;
class Check {
static object? consume(object? value = null) => null;
    public static void Main() {
JsonNode? shared = (JsonNode?)null;
consume(new JsonObject {["left"] = ((JsonNode?)shared)?.DeepClone(), ["nested"] = new JsonArray {((JsonNode?)shared)?.DeepClone()}});
    }
}
