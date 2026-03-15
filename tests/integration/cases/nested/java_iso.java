import java.time.Instant;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.time.ZoneId;
import java.util.Map;
class Check {
    Object x = Map.ofEntries(
    Map.entry("users", new Object[]{Map.ofEntries(Map.entry("name", "Bob"), Map.entry("tags", new Object[]{"admin", "user"})), Map.ofEntries(Map.entry("name", "Carol"), Map.entry("tags", new Object[]{"guest"}))})
);
}
