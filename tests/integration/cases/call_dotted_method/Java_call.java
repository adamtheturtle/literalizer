class Check {
static class ClientType_ { Object send(Object... args) { return null; } }
static class NsType_ { ClientType_ client = new ClientType_(); }
static NsType_ ns = new NsType_();
    public static void check() {
ns.client.send("hello");
ns.client.send(42);
ns.client.send(true);
    }
}
