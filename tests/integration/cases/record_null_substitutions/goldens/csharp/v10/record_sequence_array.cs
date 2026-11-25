using System.Collections.Generic;
record Record0(int Replacement, int Present);
class Check {
    public static void Main() {
var my_data = new Dictionary<string, object> {
    ["rows"] = new[] {new Record0(-1, 1), new Record0(2, 3)}
};
    _ = my_data;
    }
}
