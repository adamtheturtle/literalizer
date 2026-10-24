using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["__proto__"] = new JsonObject {["x"] = 1},
    ["ordinary"] = 2
};
    _ = my_data;
