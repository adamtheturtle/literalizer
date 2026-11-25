using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["test"] = new JsonArray {5, new JsonArray {"compile", "test"}},
    ["package"] = new JsonArray {7, new JsonArray {"link", "test"}}
};
    _ = my_data;
