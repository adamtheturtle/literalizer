using System.Text.Json.Nodes;
class Check {
class ThingType_ { public object? go(object? before = null, object? populated = null, object? after = null) => null; }
static ThingType_ thing = new ThingType_();
    public static void Main() {
thing.go(new JsonArray(), new JsonArray {1}, new JsonArray());
thing.go(new JsonArray {"text"}, new JsonArray {2}, new JsonArray());
thing.go(new JsonArray(), new JsonArray {"text"}, new JsonArray());
thing.go(new JsonArray {"text"}, new JsonArray {2}, new JsonArray {3});
    }
}
