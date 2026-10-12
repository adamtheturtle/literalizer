using System.Text.Json.Nodes;
class Check {
static object process(object value = null) => null;
    public static void Main() {
JsonNode? arena = new JsonObject {
    ["a"] = 1
};
JsonNode? ZVal = new JsonObject {
    ["a"] = 1
};
JsonNode? ZKV = new JsonObject {
    ["a"] = 1
};
process(arena);
process(ZVal);
process(ZKV);
    }
}
