using System.Text.Json.Nodes;
JsonNode? Shared = new JsonObject {
    ["field"] = new JsonArray {1, 2}
};
JsonNode? my_data = ((JsonNode?)Shared)?.DeepClone();
    _ = my_data;
