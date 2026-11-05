using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["exact_millisecond"] = "09:30:15.123000",
    ["sub_millisecond"] = "09:30:15.123456"
};
    _ = my_data;
