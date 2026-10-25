using System.Text.Json.Nodes;
JsonNode? Shared = new JsonArray {
    1,
    2
};
JsonNode? Build = new JsonArray {
    1,
    2
};
JsonNode? JsonObject = new JsonArray {
    1,
    2
};
JsonNode? JsonAllocator = new JsonArray {
    1,
    2
};
JsonNode? JsonEntries = new JsonArray {
    1,
    2
};
JsonNode? JsonEntry = new JsonArray {
    1,
    2
};
JsonNode? my_data = new JsonObject {
    ["field"] = ((JsonNode?)Shared)?.DeepClone(),
    ["nested"] = new JsonArray {((JsonNode?)Shared)?.DeepClone(), new JsonObject()},
    ["build"] = ((JsonNode?)Build)?.DeepClone(),
    ["json_object"] = ((JsonNode?)JsonObject)?.DeepClone(),
    ["json_allocator"] = ((JsonNode?)JsonAllocator)?.DeepClone(),
    ["json_entries"] = ((JsonNode?)JsonEntries)?.DeepClone(),
    ["json_entry"] = ((JsonNode?)JsonEntry)?.DeepClone()
};
    _ = my_data;
