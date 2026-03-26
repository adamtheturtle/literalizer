import java.util.Map;
class Check {
    public static void check() {
var my_data = new Object[]{
    Map.ofEntries(Map.entry("type", "create"), Map.entry("pr_id", "pr_1"), Map.entry("draft", true)),
    Map.ofEntries(Map.entry("type", "create"), Map.entry("pr_id", "pr_2"))
};
my_data = new Object[]{
    Map.ofEntries(Map.entry("type", "create"), Map.entry("pr_id", "pr_1"), Map.entry("draft", true)),
    Map.ofEntries(Map.entry("type", "create"), Map.entry("pr_id", "pr_2"))
};
    }
}
