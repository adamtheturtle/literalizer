import java.time.Instant;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("ts", Instant.parse("3000-12-31T23:59:59.999999+00:00"))
);
    }
}
