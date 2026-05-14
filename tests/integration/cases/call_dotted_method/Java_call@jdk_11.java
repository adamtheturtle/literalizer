class Main {
static class ClientType_ { Object fetch(Object... args) { return null; } }
static class AppType_ { ClientType_ client = new ClientType_(); }
static AppType_ app = new AppType_();
    public static void main() {
app.client.fetch("hello");
app.client.fetch(42);
app.client.fetch(true);
    }
}
