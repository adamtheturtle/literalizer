using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["x"] = "\u0085"
};
    _ = my_data;
