import java.time.LocalDate;
import java.time.Instant;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("ancient_date", LocalDate.of(1500, 3, 1)),
    Map.entry("modern_date", LocalDate.of(2024, 1, 15)),
    Map.entry("before_date", LocalDate.of(1582, 10, 4)),
    Map.entry("gap_date", LocalDate.of(1582, 10, 10)),
    Map.entry("transition_date", LocalDate.of(1582, 10, 15)),
    Map.entry("after_date", LocalDate.of(1582, 10, 16)),
    Map.entry("before_naive", Instant.parse("1582-10-04T12:30:00.000001Z")),
    Map.entry("gap_naive", Instant.parse("1582-10-10T12:30:00.500000Z")),
    Map.entry("transition_positive", Instant.parse("1582-10-15T00:30:00+18:00")),
    Map.entry("transition_negative", Instant.parse("1582-10-15T23:30:00-18:00")),
    Map.entry("after_positive", Instant.parse("1582-10-16T00:30:00+18:00"))
);
    }
}
