import java.time.LocalDate;
import java.time.ZoneId;
import java.time.ZonedDateTime;
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
    Map.entry("before_naive", ZonedDateTime.of(1582, 10, 4, 12, 30, 0, 1000, ZoneId.of("UTC"))),
    Map.entry("gap_naive", ZonedDateTime.of(1582, 10, 10, 12, 30, 0, 500000000, ZoneId.of("UTC"))),
    Map.entry("transition_positive", ZonedDateTime.of(1582, 10, 15, 0, 30, 0, 0, ZoneId.of("+18:00"))),
    Map.entry("transition_negative", ZonedDateTime.of(1582, 10, 15, 23, 30, 0, 0, ZoneId.of("-18:00"))),
    Map.entry("after_positive", ZonedDateTime.of(1582, 10, 16, 0, 30, 0, 0, ZoneId.of("+18:00")))
);
    }
}
