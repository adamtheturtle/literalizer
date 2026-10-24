import java.util.HashMap;
import java.util.Map;
class Main {
    public static void main() {
var my_data = new HashMap<>(Map.ofEntries(
    Map.entry("__proto__", new HashMap<>(Map.ofEntries(Map.entry("x", 1)))),
    Map.entry("n", new HashMap<>(Map.ofEntries(Map.entry("__proto__", 3)))),
    Map.entry("y", 2)
));
    }
}
