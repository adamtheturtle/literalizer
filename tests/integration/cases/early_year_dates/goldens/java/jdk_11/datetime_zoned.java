import java.time.LocalDate;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("date", LocalDate.of(99, 5, 27)),
    Map.entry("naive", ZonedDateTime.of(1, 1, 1, 12, 30, 0, 0, ZoneId.of("UTC"))),
    Map.entry("recent", ZonedDateTime.of(2024, 5, 27, 10, 0, 0, 0, ZoneId.of("UTC")))
);
    }
}
