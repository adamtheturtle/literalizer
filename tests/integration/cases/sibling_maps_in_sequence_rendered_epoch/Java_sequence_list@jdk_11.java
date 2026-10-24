import java.time.Instant;
import java.util.Map;
import java.util.List;
class Main {
    public static void main() {
var my_data = List.of(
    Map.ofEntries(Map.entry("k", Instant.parse("2040-01-01T00:00:00+00:00"))),
    Map.ofEntries(Map.entry("k", 1))
);
    }
}
