class Main {
static class ClientType_ { Object fetch(Object... args) { return null; } }
static class AppType_ { ClientType_ client = new ClientType_(); }
static AppType_ app = new AppType_();
static Object emit(Object... args) { return null; }
    public static void main() {
emit(app.client.fetch("hello"));
emit(app.client.fetch(42));
emit(app.client.fetch(true));
    }
}
