using System.Text.Json.Nodes;
JsonNode? Shared = (JsonNode?)null;
JsonNode? my_data = ((JsonNode?)Shared)?.DeepClone();
    _ = my_data;
