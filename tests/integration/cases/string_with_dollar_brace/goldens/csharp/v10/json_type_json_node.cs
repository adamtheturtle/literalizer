using System.Text.Json.Nodes;
JsonNode? my_data = new JsonArray {
    "prefix ${HOME} suffix",
    "${interpolated}"
};
    _ = my_data;
