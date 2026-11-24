using System.Text.Json.Nodes;
        JsonNode? Shared = new JsonArray {
            1,
            2
        };
        JsonNode? my_data = new JsonObject {
            ["field"] = new JsonObject {["nested"] = ((JsonNode?)Shared)?.DeepClone()},
            ["text"] = "first\n{ \" // }"
        };
    _ = my_data;
