import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
class Main {
    public static void main() {
var my_data = new HashMap<>(Map.ofEntries(
    Map.entry("b", new HashMap<>(Map.ofEntries(Map.entry("k", 1)))),
    Map.entry("a", new HashMap<>(Map.ofEntries(Map.entry("k", Instant.parse("2040-01-01T00:00:00+00:00")))))
));
    }
}
