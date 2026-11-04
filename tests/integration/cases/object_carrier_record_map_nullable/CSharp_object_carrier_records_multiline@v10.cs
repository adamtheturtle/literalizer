using System.Collections.Generic;
record Record0(Dictionary<string, object?> Payload);
class Example {
    static void Main() {
var my_data = new[] {
    new Record0(
        new Dictionary<string, object?> {
            ["flag"] = true
        }
    ),
    new Record0(
        new Dictionary<string, object?> {
            ["nothing"] = (object?)null
        }
    )
};
        System.Collections.Generic.Dictionary<string, object?> first = my_data[0].Payload;
        System.Collections.Generic.Dictionary<string, object?> second = my_data[1].Payload;
        if (first["flag"] is not true || second["nothing"] is not null) { throw new System.InvalidOperationException("changed record maps"); }
    }
}
