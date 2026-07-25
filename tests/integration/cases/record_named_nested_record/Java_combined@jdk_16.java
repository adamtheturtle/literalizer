import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("collection", "alpha"),
    Map.entry("featured_entry", Map.ofEntries(Map.entry("id", 100), Map.entry("label", "first entry"), Map.entry("enabled", false), Map.entry("related_ids", new int[]{102, 103})))
);
my_data = Map.ofEntries(
    Map.entry("collection", "alpha"),
    Map.entry("featured_entry", Map.ofEntries(Map.entry("id", 100), Map.entry("label", "first entry"), Map.entry("enabled", false), Map.entry("related_ids", new int[]{102, 103})))
);
    }
}
