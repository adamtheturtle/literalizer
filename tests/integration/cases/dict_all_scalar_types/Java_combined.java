import java.time.LocalDate;
import java.time.Instant;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("s", "string"),
    Map.entry("i", 1),
    Map.entry("f", 1.5),
    Map.entry("b", true),
    Map.entry("d", LocalDate.of(2024, 1, 15)),
    Map.entry("dt", Instant.parse("2024-01-15T12:00:00Z")),
    Map.entry("by", "48656c6c6f")
);
my_data = Map.ofEntries(
    Map.entry("s", "string"),
    Map.entry("i", 1),
    Map.entry("f", 1.5),
    Map.entry("b", true),
    Map.entry("d", LocalDate.of(2024, 1, 15)),
    Map.entry("dt", Instant.parse("2024-01-15T12:00:00Z")),
    Map.entry("by", "48656c6c6f")
);
    }
}
