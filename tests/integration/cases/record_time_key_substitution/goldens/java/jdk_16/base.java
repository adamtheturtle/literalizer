import java.time.LocalTime;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("value", Map.ofEntries(Map.entry(LocalTime.of(1, 2, 3), 1)))
);
    }
}
