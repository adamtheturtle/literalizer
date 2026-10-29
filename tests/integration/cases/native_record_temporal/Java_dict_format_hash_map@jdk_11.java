import java.time.LocalTime;
import java.time.LocalDate;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
class Main {
    public static void main() {
var my_data = new HashMap<>(Map.ofEntries(
    Map.entry("birthday", LocalDate.of(2024, 1, 15)),
    Map.entry("meeting", LocalTime.of(9, 30)),
    Map.entry("event_time", Instant.parse("2024-01-15T12:30:00+00:00"))
));
    }
}
