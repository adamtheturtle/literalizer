using System.Text.Json.Nodes;
JsonNode? Shared = new JsonArray {
    1,
    2
};
JsonNode? my_data = new JsonArray {
    ((JsonNode?)Shared)?.DeepClone(),
    42
};
    _ = my_data;
