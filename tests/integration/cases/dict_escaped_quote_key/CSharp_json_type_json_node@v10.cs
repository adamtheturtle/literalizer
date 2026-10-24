using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["a\"b"] = 1
};
    _ = my_data;
