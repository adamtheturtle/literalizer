import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("project", "alpha"),
    Map.entry("lead_item", Map.ofEntries(Map.entry("id", 100), Map.entry("label", "first item"), Map.entry("enabled", false), Map.entry("related_ids", new int[]{102, 103})))
);
my_data = Map.ofEntries(
    Map.entry("project", "alpha"),
    Map.entry("lead_item", Map.ofEntries(Map.entry("id", 100), Map.entry("label", "first item"), Map.entry("enabled", false), Map.entry("related_ids", new int[]{102, 103})))
);
    }
}
