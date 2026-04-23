import java.util.Map;
class Check {
static class MgrType_ { Object Op(Object... args) { return null; } }
static MgrType_ mgr = new MgrType_();
    public static void check() {
mgr.Op(Map.ofEntries(Map.entry("type", "create"), Map.entry("pr_id", "pr_1"), Map.entry("draft", true)));
mgr.Op(Map.ofEntries(Map.entry("type", "create"), Map.entry("pr_id", "pr_2")));
    }
}
