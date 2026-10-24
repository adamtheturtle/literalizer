import java.util.Map;
class Main {
    public static void main() {
Map<String, Map<String, Integer>> my_data = Map.ofEntries(
    Map.entry("_", Map.ofEntries(Map.entry("a", 1), Map.entry("b", 2)))
);
    }
}
