using System.Text.Json.Nodes;
class Check {
static object process(object value = null) => null;
    public static void Main() {
process((JsonNode?)("hello"));
process((JsonNode?)(42));
process((JsonNode?)(true));
    }
}
