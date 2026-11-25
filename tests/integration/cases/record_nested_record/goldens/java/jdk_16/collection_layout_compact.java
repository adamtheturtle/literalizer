import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("id", 1),
    Map.entry("owner", Map.ofEntries(Map.entry("name", "Alice"), Map.entry("age", 30)))
);
    }
}
