using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["a"] = new JsonArray {new JsonObject {["item"] = new JsonArray {1}}},
    ["b"] = new JsonArray {new JsonObject {["item"] = new JsonArray {2, 3}}}
};
    _ = my_data;
