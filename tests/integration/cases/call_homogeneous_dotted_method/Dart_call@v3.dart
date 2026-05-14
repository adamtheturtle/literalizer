class _ClientType { dynamic fetch({dynamic value}) => null; }
class _AppType { final client = _ClientType(); }
final app = _AppType();
final my_data = null;
void main() {
    app.client.fetch(value: "hello");
    app.client.fetch(value: "world");
}
