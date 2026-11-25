class _WorkerType { dynamic process({dynamic values, dynamic count}) => null; }
class _ApiType { final worker = _WorkerType(); }
final api = _ApiType();
final my_data = null;
void main() {
    api.worker.process(values: [1, <String, dynamic>{}], count: 42);
    api.worker.process(values: [2, <String, String>{"x": "s"}], count: 43);
}
