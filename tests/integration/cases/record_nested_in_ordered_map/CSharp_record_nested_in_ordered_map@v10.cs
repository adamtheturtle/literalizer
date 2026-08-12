using System.Collections.Generic;
record Record0(object Name, int Id);
class Check {
    public static void Main() {
var my_data = new Dictionary<string, object> {
    ["outer"] = new[] {new Record0((object?)null, 1)}
};
    }
}
