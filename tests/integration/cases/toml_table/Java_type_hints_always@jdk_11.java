import java.util.Map;
class Main {
    public static void main() {
Map<String, Map<String, Integer>> my_data = Map.ofEntries(
    Map.entry("section", Map.ofEntries(Map.entry("value", 1)))
);
    }
}
