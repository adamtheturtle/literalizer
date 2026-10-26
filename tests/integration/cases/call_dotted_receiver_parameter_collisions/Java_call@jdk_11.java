import java.util.Map;
class Main {
static class WorkerType_ { Object process(Object arg0, Object arg1) { return null; } }
static class ApiType_ { WorkerType_ worker = new WorkerType_(); }
static ApiType_ api = new ApiType_();
    public static void main() {
api.worker.process(Map.ofEntries(), Map.ofEntries());
    }
}
