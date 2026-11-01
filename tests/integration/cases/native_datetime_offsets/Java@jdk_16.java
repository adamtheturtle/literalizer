import java.time.Instant;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("stamps", new Object[]{Instant.parse("2001-02-03T04:05:06+00:00:01"), Instant.parse("2001-02-03T04:05:06-00:00:01"), Instant.parse("2001-02-03T04:05:06+00:00:00.000001"), Instant.parse("2001-02-03T04:05:06-00:00:00.000001"), Instant.parse("2001-02-03T04:05:06+05:30:15.000001"), Instant.parse("2001-02-03T04:05:06-05:30:15.000001")})
);
    }
}
