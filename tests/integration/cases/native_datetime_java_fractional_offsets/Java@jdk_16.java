import java.time.Instant;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("stamps", new Object[]{Instant.parse("2001-02-03T04:05:06.123456+00:00"), Instant.parse("2001-02-03T04:05:06.123456+00:00:01"), Instant.parse("2001-02-03T04:05:06.123456-00:00:01"), Instant.parse("2001-02-03T04:05:06.123455+00:00"), Instant.parse("2001-02-03T04:05:06.123457+00:00"), Instant.parse("2001-02-02T22:34:51.123455+00:00"), Instant.parse("2001-02-03T09:35:21.123457+00:00")})
);
    }
}
