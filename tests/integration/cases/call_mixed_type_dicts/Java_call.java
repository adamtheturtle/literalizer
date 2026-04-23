import java.util.Map;
class Check {
static class MType_ { Object Op(Object... args) { return null; } }
static MType_ m = new MType_();
    public static void check() {
m.Op(Map.ofEntries(Map.entry("type", "create"), Map.entry("pr_id", "pr_1"), Map.entry("draft", true)));
m.Op(Map.ofEntries(Map.entry("type", "create"), Map.entry("pr_id", "pr_2")));
    }
}
