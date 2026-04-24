using System;
class Check {
class ClientType_ { public object fetch(object payload = null) => null; }
class AppType_ { public ClientType_ client = new ClientType_(); }
static AppType_ app = new AppType_();
    public static void Main() {
app.client.fetch("hello");
app.client.fetch(42);
app.client.fetch(true);
    }
}
