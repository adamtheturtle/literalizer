using System.Text.Json.Nodes;
JsonNode? my_data = new JsonArray {
    "This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.",
    1
};
    _ = my_data;
