import java.util.HashMap;
import java.util.Map;
class Main {
    public static void main() {
var my_data = new HashMap<>(Map.ofEntries(
    Map.entry("a", new Object[]{new HashMap<>(Map.ofEntries(Map.entry("item", new int[]{1})))}),
    Map.entry("b", new Object[]{new HashMap<>(Map.ofEntries(Map.entry("item", new int[]{2})))})
));
    }
}
