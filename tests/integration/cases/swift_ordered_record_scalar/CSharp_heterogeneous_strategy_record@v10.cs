using System.Collections.Generic;
record Record0(int Id);
class Check {
    public static void Main() {
var my_data = new Dictionary<string, object> {
    ["first"] = new[] {new Record0(1)},
    ["second"] = 2
};
    }
}
