using System.Collections.Generic;
record Record0(int X);
class Check {
    public static void Main() {
var my_data = new object[] {
    new Dictionary<string, object> {["first"] = new Record0(1)},
    new Dictionary<string, object> {["first"] = new Record0(2)}
};
    _ = my_data;
    }
}
