import java.time.Instant;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("half", Instant.parse("1979-05-27T07:32:00.500000Z")),
    Map.entry("milli", Instant.parse("1979-05-27T07:32:00.100000Z")),
    Map.entry("max_milli", Instant.parse("1979-05-27T07:32:00.999000Z")),
    Map.entry("whole", Instant.parse("1979-05-27T07:32:00Z"))
);
    }
}
