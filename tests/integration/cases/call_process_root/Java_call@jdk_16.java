import java.util.Map;
class Main {
static class ApiType_ { Object fetch(Object arg0) { return null; } }
static class ProcessType_ { ApiType_ api = new ApiType_(); }
static ProcessType_ process = new ProcessType_();
    public static void main() {
process.api.fetch(Map.ofEntries(Map.entry("data", "hello")));
process.api.fetch(Map.ofEntries(Map.entry("data", 42)));
process.api.fetch(Map.ofEntries(Map.entry("data", true)));
    }
}
