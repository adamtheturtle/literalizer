using System;
class Check {
class ClientType_ { public object? go(object? first_value = null, object? second_value = null) => null; }
class AppType_ { public ClientType_ client = new ClientType_(); }
static AppType_ app = new AppType_();
    public static void Main() {
app.client.go(ValueTuple.Create(1), ValueTuple.Create("text"));
    }
}
