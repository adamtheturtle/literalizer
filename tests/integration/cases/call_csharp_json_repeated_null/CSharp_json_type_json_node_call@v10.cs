using System.Text.Json.Nodes;
class Check {
static object consume(object value = null) => null;
    public static void Main() {
JsonNode? shared = (JsonNode?)null;
consume(new JsonObject {["left"] = shared?.DeepClone(), ["nested"] = new JsonArray {shared?.DeepClone()}});
    }
}
