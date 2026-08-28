using System.Collections.Generic;
record Record1(string Kind, bool Urgent);
record Record0(Record1[] Entries);
record Record3(string Error);
record Record2(Record3[] Entries);
class Check {
    public static void Main() {
var my_data = new Dictionary<string, object> {
    ["left"] = new Record0(new[] {new Record1("add", true)}),
    ["right"] = new Record2(new[] {new Record3("not_found")})
};
    }
}
