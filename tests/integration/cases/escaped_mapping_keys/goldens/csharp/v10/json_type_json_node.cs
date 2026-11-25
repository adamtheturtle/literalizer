using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["quote\"backslash\\"] = 1,
    ["line\nbreak"] = 2,
    ["$(literal)${text}"] = 3,
    ["RStr prefix"] = 4
};
    _ = my_data;
