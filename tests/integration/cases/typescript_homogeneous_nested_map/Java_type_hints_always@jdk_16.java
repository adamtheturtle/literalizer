import java.util.Map;
class Main {
    public static void main() {
Map<String, Map<String, Integer>> my_data = Map.ofEntries(
    Map.entry("first", Map.ofEntries(Map.entry("x", 1), Map.entry("y", 2))),
    Map.entry("second", Map.ofEntries(Map.entry("z", 3)))
);
    }
}
