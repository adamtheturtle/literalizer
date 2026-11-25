class _ApiType { dynamic fetch({dynamic data}) => null; }
class _ProcessType { final api = _ApiType(); }
final process = _ProcessType();
final my_data = null;
void main() {
    process.api.fetch(data: <String, dynamic>{"data": "hello"});
    process.api.fetch(data: <String, dynamic>{"data": 42});
    process.api.fetch(data: <String, dynamic>{"data": true});
}
