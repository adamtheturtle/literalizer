using System.Text.Json.Nodes;
JsonNode? Shared = (JsonNode?)(42);
JsonNode? my_data = new JsonArray {
    ((JsonNode?)Shared)?.DeepClone(),
    ((JsonNode?)Shared)?.DeepClone()
};
    _ = my_data;
