using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["fffe"] = "￾",
    ["ffff"] = "￿"
};
    _ = my_data;
