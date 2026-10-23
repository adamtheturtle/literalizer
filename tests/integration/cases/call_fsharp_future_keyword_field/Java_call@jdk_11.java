import java.util.Map;
class Main {
static class ProcessType_ { Object fetch(Object arg0) { return null; } }
static class AppType_ { ProcessType_ process = new ProcessType_(); }
static AppType_ app = new AppType_();
    public static void main() {
app.process.fetch(Map.ofEntries(Map.entry("data", "hello")));
app.process.fetch(Map.ofEntries(Map.entry("data", 42)));
app.process.fetch(Map.ofEntries(Map.entry("data", true)));
    }
}
