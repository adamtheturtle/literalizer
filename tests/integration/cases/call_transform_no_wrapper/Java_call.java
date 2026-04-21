class Check {
static class ApiType_ { Object request(Object... args) { return null; } }
static class ClientType_ { ApiType_ api = new ApiType_(); }
static ClientType_ client = new ClientType_();
    public static void check() {
client.api.request("hello");
client.api.request(42);
client.api.request(true);
    }
}
