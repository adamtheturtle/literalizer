import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("level1", Map.ofEntries(Map.entry("level2", Map.ofEntries(Map.entry("level3", Map.ofEntries(Map.entry("level4", Map.ofEntries(Map.entry("value", "deep"), Map.entry("items", new String[]{"a", "b"}))))), Map.entry("sibling", 42))), Map.entry("tags", new Object[]{Map.ofEntries(Map.entry("name", "tag1"), Map.entry("meta", Map.ofEntries(Map.entry("priority", 1), Map.entry("labels", new String[]{"x", "y"}))))})))
);
    }
}
