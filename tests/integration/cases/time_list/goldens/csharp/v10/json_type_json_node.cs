using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["times"] = new JsonArray {"09:30:00", "17:45:00", "23:59:59"}
};
    _ = my_data;
