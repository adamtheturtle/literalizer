using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["name"] = "Alice",
    ["scores"] = new JsonArray {10, 20, 30}
};
