using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["x"] = "before\0after"
};
    _ = my_data;
