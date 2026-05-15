import java.util.HashMap;
import java.util.Map;
class Main {
    public static void main() {
HashMap<String, Object> my_data = new HashMap<>(Map.ofEntries(
    Map.entry("name", "Alice"),
    Map.entry("age", 30),
    Map.entry("active", true)
));
    }
}
