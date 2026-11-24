import java.util.HashMap;
import java.util.Map;
class Main {
    public static void main() {
var my_data = new HashMap<>(Map.ofEntries(
    Map.entry("test", new Object[]{5, new String[]{"compile", "test"}}),
    Map.entry("package", new Object[]{7, new String[]{"link", "test"}})
));
    }
}
