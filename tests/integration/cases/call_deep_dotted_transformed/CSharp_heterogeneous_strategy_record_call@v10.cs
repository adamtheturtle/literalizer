class Check {
class ClientType_ { public object fetch(object payload = null) => null; }
class AppType_ { public ClientType_ client = new ClientType_(); }
static AppType_ app = new AppType_();
static object emit(object _arg = null) => null;
    public static void Main() {
emit(app.client.fetch("hello"));
emit(app.client.fetch(42));
emit(app.client.fetch(true));
    }
}
