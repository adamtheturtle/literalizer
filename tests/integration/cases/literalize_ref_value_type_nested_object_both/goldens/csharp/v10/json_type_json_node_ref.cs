using System.Text.Json.Nodes;
JsonNode? Shared = new JsonArray {
    1,
    2
};
JsonNode? my_data = new JsonObject {
    ["field"] = ((JsonNode?)Shared)?.DeepClone()
};
my_data = new JsonObject {
    ["field"] = ((JsonNode?)Shared)?.DeepClone()
};
    _ = my_data;
