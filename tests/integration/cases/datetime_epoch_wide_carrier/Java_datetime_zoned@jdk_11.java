import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("within_i32", ZonedDateTime.of(2024, 1, 15, 12, 0, 0, 0, ZoneId.of("UTC"))),
    Map.entry("beyond_i32", ZonedDateTime.of(2099, 6, 15, 8, 30, 0, 0, ZoneId.of("UTC")))
);
    }
}
