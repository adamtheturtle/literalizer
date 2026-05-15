import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("project", "alpha"),
    Map.entry("lead_task", Map.ofEntries(Map.entry("id", 100), Map.entry("description", "first task"), Map.entry("is_done", false), Map.entry("blocks", new int[]{102, 103})))
);
    }
}
