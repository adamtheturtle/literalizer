import java.time.LocalTime;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", Map.ofEntries(Map.entry("k", LocalTime.of(7, 30)))),
    Map.entry("b", Map.ofEntries(Map.entry("k", "string")))
);
    }
}
