using System.Collections.Generic;
record Record0(int Id, string Label, object[] Tags);
class Check {
    public static void Main() {
var my_data = new[] {
    new Record0(1, "first", new object[] {}),
    new Record0(2, "second", new object[] {}),
    new Record0(3, "third", new object[] {})
};
    }
}
