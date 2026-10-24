import java.util.Map;
class Main {
    public static void main() {
Map<String, Object> my_data = Map.ofEntries(
    Map.entry("__proto__", Map.ofEntries(Map.entry("x", 1))),
    Map.entry("n", Map.ofEntries(Map.entry("__proto__", 3))),
    Map.entry("y", 2)
);
    }
}
