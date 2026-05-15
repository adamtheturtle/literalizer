import java.util.Map;
class Main {
static Object process(Object... args) { return null; }
    public static void main() {
// Test cases
process(Map.ofEntries(Map.entry("type", "create"), Map.entry("pr_id", "pr_1")));  // first case
process(Map.ofEntries(Map.entry("type", "update"), Map.entry("pr_id", "pr_2")));  // second case
// third case
process(Map.ofEntries(Map.entry("type", "delete"), Map.entry("pr_id", "pr_3")));
    }
}
