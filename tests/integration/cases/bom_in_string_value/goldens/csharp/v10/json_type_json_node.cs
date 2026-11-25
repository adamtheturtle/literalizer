using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["v"] = "a﻿b"
};
    _ = my_data;
