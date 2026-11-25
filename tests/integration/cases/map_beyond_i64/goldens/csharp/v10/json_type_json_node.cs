using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["a"] = 9223372036854775807UL,
    ["b"] = 9223372036854775808UL
};
    _ = my_data;
