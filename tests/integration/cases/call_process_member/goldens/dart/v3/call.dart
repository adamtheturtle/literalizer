class _ProcessType { dynamic fetch({dynamic data}) => null; }
class _AppType { final process = _ProcessType(); }
final app = _AppType();
final my_data = null;
void main() {
    app.process.fetch(data: <String, dynamic>{"data": "hello"});
    app.process.fetch(data: <String, dynamic>{"data": 42});
    app.process.fetch(data: <String, dynamic>{"data": true});
}
