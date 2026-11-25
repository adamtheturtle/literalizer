class Main {
static class ClientType_ { Object go(Object arg0, Object arg1) { return null; } }
static class AppType_ { ClientType_ client = new ClientType_(); }
static AppType_ app = new AppType_();
    public static void main() {
app.client.go(new int[]{1}, new int[]{2});
    }
}
