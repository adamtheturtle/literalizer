using System.Collections.Generic;
var my_data = new Dictionary<string, object?> {
    // A JSONC input case with both comment forms.
    ["url"] = "https://example.org/a/*b*/",  // detail
    // continued
    ["count"] = 0b10  // trailing line comment
};
    _ = my_data;
