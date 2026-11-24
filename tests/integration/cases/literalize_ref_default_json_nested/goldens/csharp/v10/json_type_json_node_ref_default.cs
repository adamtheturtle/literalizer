using System.Text.Json.Nodes;
JsonNode? shared = (JsonNode?)(42);
JsonNode? my_data = new JsonObject {
    ["refs"] = new JsonArray {((JsonNode?)shared)?.DeepClone(), ((JsonNode?)shared)?.DeepClone()},
    ["quoted"] = "#{shared}"
};
    _ = my_data;
