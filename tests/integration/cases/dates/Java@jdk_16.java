import java.time.LocalDate;
import java.time.Instant;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("date", LocalDate.of(2024, 1, 15)),
    Map.entry("datetime", Instant.parse("2024-01-15T12:30:00+00:00"))
);
    }
}
