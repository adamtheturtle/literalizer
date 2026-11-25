class _ClientType { dynamic go({dynamic first_value, dynamic second_value}) => null; }
class _AppType { final client = _ClientType(); }
final app = _AppType();
final my_data = null;
void main() {
    app.client.go(first_value: <int>[1], second_value: <String>["text"]);
}
