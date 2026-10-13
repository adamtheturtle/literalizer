#nullable enable annotations
using System.Text.Json.Nodes;
class Check {
static object consume(object value = null) => null;
    public static void Main() {
JsonNode? shared = new JsonObject {
    ["value"] = new JsonArray {1, 2}
};
consume(new JsonObject {["left"] = ((JsonNode?)shared)?.DeepClone(), ["right"] = ((JsonNode?)shared)?.DeepClone()});
    }
}
