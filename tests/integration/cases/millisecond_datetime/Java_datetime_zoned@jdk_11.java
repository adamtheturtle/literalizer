import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("half", ZonedDateTime.of(1979, 5, 27, 7, 32, 0, 500000000, ZoneId.of("UTC"))),
    Map.entry("milli", ZonedDateTime.of(1979, 5, 27, 7, 32, 0, 100000000, ZoneId.of("UTC"))),
    Map.entry("max_milli", ZonedDateTime.of(1979, 5, 27, 7, 32, 0, 999000000, ZoneId.of("UTC"))),
    Map.entry("whole", ZonedDateTime.of(1979, 5, 27, 7, 32, 0, 0, ZoneId.of("UTC")))
);
    }
}
