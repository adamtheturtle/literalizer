import java.util.HashMap;
import java.util.Map;
class Main {
    public static void main() {
var my_data = new HashMap<>(Map.ofEntries(
    Map.entry("outer", new HashMap<>(Map.ofEntries(Map.entry("a", 1), Map.entry("b", "x"))))
));
    }
}
