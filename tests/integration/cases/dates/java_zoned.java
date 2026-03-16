import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.Set;
class Check {
    Object x = Map.ofEntries(
    Map.entry("date", LocalDate.of(2024, 1, 15)),
    Map.entry("datetime", ZonedDateTime.of(2024, 1, 15, 12, 30, 0, 0, ZoneId.of("+00:00")))
);
}
