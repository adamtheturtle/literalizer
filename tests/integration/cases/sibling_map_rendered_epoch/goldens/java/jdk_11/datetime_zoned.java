import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", Map.ofEntries(Map.entry("k", ZonedDateTime.of(2040, 1, 1, 0, 0, 0, 0, ZoneId.of("Z"))))),
    Map.entry("b", Map.ofEntries(Map.entry("k", 1)))
);
    }
}
