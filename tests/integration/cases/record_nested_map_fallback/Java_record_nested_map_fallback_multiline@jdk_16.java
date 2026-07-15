import java.util.Map;
record Record0(String name, java.util.Map<String, Object> input, java.util.Map<String, Object> expected) {}
class Main {
    public static void main() {
var my_data = new Object[]{
    new Record0(
        "test_1",
        Map.ofEntries(
            Map.entry("type", "create"),
            Map.entry("pr_id", "pr_1"),
            Map.entry("draft", true)
        ),
        Map.ofEntries(
            Map.entry("pr_id", "pr_1"),
            Map.entry("status", "draft")
        )
    ),
    new Record0(
        "test_2",
        Map.ofEntries(
            Map.entry("type", "publish"),
            Map.entry("pr_id", "pr_1")
        ),
        Map.ofEntries(
            Map.entry("error", "invalid_operation")
        )
    )
};
    }
}
