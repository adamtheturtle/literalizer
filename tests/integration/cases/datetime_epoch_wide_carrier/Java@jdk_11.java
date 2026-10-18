import java.time.Instant;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("within_i32", Instant.parse("2024-01-15T12:00:00Z")),
    Map.entry("beyond_i32", Instant.parse("2099-06-15T08:30:00Z"))
);
    }
}
