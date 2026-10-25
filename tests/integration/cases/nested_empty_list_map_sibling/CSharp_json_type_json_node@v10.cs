using System.Text.Json.Nodes;
JsonNode? my_data = new JsonArray {
    new JsonObject {["values"] = new JsonArray()},
    new JsonObject()
};
    _ = my_data;
