using System.Text.Json.Nodes;
JsonNode? my_data = (JsonNode?)("a\u0085b\u2028c\u2029d\r\u2028e");
    _ = my_data;
