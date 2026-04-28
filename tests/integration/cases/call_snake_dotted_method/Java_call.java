class Main {
static class Http_ClientType_ { Object fetch(Object... args) { return null; } }
static class My_AppType_ { Http_ClientType_ http_client = new Http_ClientType_(); }
static My_AppType_ my_app = new My_AppType_();
    public static void main() {
my_app.http_client.fetch("hello");
my_app.http_client.fetch(42);
my_app.http_client.fetch(true);
    }
}
