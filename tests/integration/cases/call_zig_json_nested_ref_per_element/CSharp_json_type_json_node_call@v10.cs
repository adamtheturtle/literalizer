using System.Text.Json.Nodes;
class Check {
static object consume(object value = null) => null;
    public static void Main() {
JsonNode? shared = new JsonArray {
    1,
    2
};
consume(new JsonObject {["field"] = shared});
consume(shared);
    }
}
