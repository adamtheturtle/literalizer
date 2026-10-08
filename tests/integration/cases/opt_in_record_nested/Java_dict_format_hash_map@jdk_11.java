import java.util.HashMap;
import java.util.Map;
class Main {
    public static void main() {
var my_data = new HashMap<>(Map.ofEntries(
    Map.entry("owner", new HashMap<>(Map.ofEntries(Map.entry("name", "Ada"), Map.entry("active", false)))),
    Map.entry("members", new Object[]{new HashMap<>(Map.ofEntries(Map.entry("name", "Ada"), Map.entry("score", 1.5))), new HashMap<>(Map.ofEntries(Map.entry("name", "Bob"), Map.entry("score", 2.5)))})
));
    }
}
