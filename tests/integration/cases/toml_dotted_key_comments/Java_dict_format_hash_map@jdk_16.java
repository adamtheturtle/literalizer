import java.util.HashMap;
import java.util.Map;
class Main {
    public static void main() {
var my_data = new HashMap<>(Map.ofEntries(
    // first dotted key
    // second dotted key
    Map.entry("a", new HashMap<>(Map.ofEntries(Map.entry("b", 1), Map.entry("c", 2))))
));
    }
}
