void main() {
struct ClientType_ { int fetch(T...)(T args) { return 0; } }
struct AppType_ { ClientType_ client; }
AppType_ app;
int emit(T...)(T args) { return 0; }
emit(app.client.fetch("hello"));
emit(app.client.fetch(42));
emit(app.client.fetch(true));
}
