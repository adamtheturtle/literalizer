using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["cr"] = "a\rb",
    ["crlf"] = "a\r\nb",
    ["lf"] = "a\nb"
};
    _ = my_data;
