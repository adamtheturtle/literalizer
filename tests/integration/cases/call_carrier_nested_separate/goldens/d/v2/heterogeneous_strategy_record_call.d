void main() {
struct ClientType_ { int go(T...)(T args) { return 0; } }
struct AppType_ { ClientType_ client; }
AppType_ app;
app.client.go([1], ["text"]);
}
