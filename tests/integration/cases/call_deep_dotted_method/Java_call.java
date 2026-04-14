class Check {
static class ClientType_ { Object post(Object... args) { return null; } }
static class ApiType_ { ClientType_ client = new ClientType_(); }
static class ObjType_ { ApiType_ api = new ApiType_(); }
static ObjType_ obj = new ObjType_();
    public static void check() {
obj.api.client.post("hello");
obj.api.client.post(42);
obj.api.client.post(true);
    }
}
