using System.Text.Json.Nodes;
JsonNode? my_data = (JsonNode?)("hello \"world\" -- not a comment");
    _ = my_data;
