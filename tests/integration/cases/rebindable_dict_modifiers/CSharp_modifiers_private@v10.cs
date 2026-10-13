#nullable enable annotations
using System.Collections.Generic;
class Check {
private Dictionary<string, int> my_data = new Dictionary<string, int> {
    // Field declaration
    ["one"] = 1,
    ["two"] = 2
};
    public Check() {
my_data = new Dictionary<string, int> {
    // Field declaration
    ["one"] = 1,
    ["two"] = 2
};
    }
    public static void Main() { }
    public void _Read_my_data() { _ = my_data; }
}
