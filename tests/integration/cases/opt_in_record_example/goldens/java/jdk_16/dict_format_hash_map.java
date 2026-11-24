import java.util.HashMap;
import java.util.Map;
class Main {
    public static void main() {
var my_data = new HashMap<>(Map.ofEntries(
    Map.entry("name", "Ada"),
    Map.entry("active", true),
    Map.entry("scores", new int[]{1, 2, 3})
));
    }
}
