using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["__proto__"] = new JsonObject {["x"] = 1},
    ["n"] = new JsonObject {["__proto__"] = 3},
    ["y"] = 2
};
    _ = my_data;
