using System.Collections.Generic;
record Record0(string Call, object[] Args);
class Check {
    public static void Main() {
var my_data = new[] {
    new Record0("send", new object[] {1, "email", "a@gmail.com", 100}),
    new Record0("recv", new object[] {2, "sms", "b@example.com", 200})
};
    }
}
