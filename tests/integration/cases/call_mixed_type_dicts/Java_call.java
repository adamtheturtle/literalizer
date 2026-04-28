import java.util.Map;
class Main {
static class MgrType_ { Object op(Object... args) { return null; } }
static class AppType_ { MgrType_ mgr = new MgrType_(); }
static AppType_ app = new AppType_();
    public static void main() {
app.mgr.op(Map.ofEntries(Map.entry("type", "create"), Map.entry("pr_id", "pr_1"), Map.entry("draft", true)));
app.mgr.op(Map.ofEntries(Map.entry("type", "create"), Map.entry("pr_id", "pr_2")));
    }
}
