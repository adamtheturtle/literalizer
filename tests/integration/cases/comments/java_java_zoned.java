import java.time.Instant;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.time.ZoneId;
import java.util.Map;
class Check {
    Object x = Map.ofEntries(
    // Server configuration
    Map.entry("host", "localhost"),  // default host
    Map.entry("port", 8080),
    // Enable debug mode
    Map.entry("debug", true)
);
}
