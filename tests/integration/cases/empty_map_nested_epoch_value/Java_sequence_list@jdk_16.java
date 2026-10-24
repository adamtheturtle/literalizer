import java.time.Instant;
import java.util.Map;
import java.util.List;
class Main {
    public static void main() {
var my_data = List.of(
    Map.ofEntries(Map.entry("nested", Map.ofEntries(Map.entry("times", List.of(Instant.parse("1900-01-01T00:00:00+00:00")))))),
    Map.ofEntries()
);
    }
}
