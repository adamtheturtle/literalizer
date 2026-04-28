import java.time.LocalDate;
import java.time.Instant;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("name", "Alice"),
    Map.entry("age", 30),
    Map.entry("active", true),
    Map.entry("joined", LocalDate.of(2024, 1, 15)),
    Map.entry("last_login", Instant.parse("2024-01-15T12:30:00+00:00")),
    Map.entry("avatar", "48656c6c6f")
);
    }
}
