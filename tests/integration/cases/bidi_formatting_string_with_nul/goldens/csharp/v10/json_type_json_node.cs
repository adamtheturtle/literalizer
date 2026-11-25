using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["v"] = "a‪\0é😀b"
};
    _ = my_data;
