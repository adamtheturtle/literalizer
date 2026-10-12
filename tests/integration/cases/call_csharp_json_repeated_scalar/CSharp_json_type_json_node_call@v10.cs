using System.Text.Json.Nodes;
class Check {
static object consume(object value = null) => null;
    public static void Main() {
JsonNode? shared = (JsonNode?)(42);
consume(new JsonArray {((JsonNode?)shared)?.DeepClone(), ((JsonNode?)shared)?.DeepClone()});
    }
}
