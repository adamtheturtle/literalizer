using System.Text.Json.Nodes;
JsonNode? Shared = (JsonNode?)("value");
JsonNode? my_data = (JsonNode?)(((JsonNode?)Shared)?.DeepClone());
    _ = my_data;
