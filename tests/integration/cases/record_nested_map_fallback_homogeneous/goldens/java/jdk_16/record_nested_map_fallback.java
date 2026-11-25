import java.util.Map;
record Record1(String kind, String pr_id) {}
record Record0(String name, Record1 input, java.util.Map<String, Object> expected) {}
class Main {
    public static void main() {
var my_data = new Record0[]{
    new Record0("test_1", new Record1("create", "pr_1"), Map.ofEntries(Map.entry("pr_id", "pr_1"), Map.entry("status", "draft"))),
    new Record0("test_2", new Record1("publish", "pr_1"), Map.ofEntries(Map.entry("error", "invalid_operation")))
};
    }
}
