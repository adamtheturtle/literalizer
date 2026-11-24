class _ClientType { dynamic fetch({dynamic payload}) => null; }
class _AppType { final client = _ClientType(); }
final app = _AppType();
final my_data = null;
void main() {
    app.client.fetch(payload: "hello");
    app.client.fetch(payload: 42);
    app.client.fetch(payload: true);
}
