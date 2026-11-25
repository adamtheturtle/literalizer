class _WorkerType { dynamic process({dynamic self, dynamic self_}) => null; }
class _ApiType { final worker = _WorkerType(); }
final api = _ApiType();
final my_data = null;
void main() {
    api.worker.process(self: <String, dynamic>{}, self_: <String, dynamic>{});
}
