using System.Text.Json.Nodes;
JsonNode? my_data = new JsonArray {
    new JsonArray {new JsonArray(), new JsonArray()},
    new JsonArray {new JsonArray {1}, new JsonArray {1}}
};
    _ = my_data;
