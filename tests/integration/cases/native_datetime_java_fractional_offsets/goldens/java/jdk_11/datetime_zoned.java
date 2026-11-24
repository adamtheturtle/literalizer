import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("stamps", new Object[]{ZonedDateTime.of(2001, 2, 3, 4, 5, 6, 123456000, ZoneId.of("UTC")), ZonedDateTime.of(2001, 2, 3, 4, 5, 6, 123456000, ZoneId.of("UTC+00:00:01")), ZonedDateTime.of(2001, 2, 3, 4, 5, 6, 123456000, ZoneId.of("UTC-00:00:01")), ZonedDateTime.of(2001, 2, 3, 4, 5, 6, 123455000, ZoneId.of("UTC")), ZonedDateTime.of(2001, 2, 3, 4, 5, 6, 123457000, ZoneId.of("UTC")), ZonedDateTime.of(2001, 2, 2, 22, 34, 51, 123455000, ZoneId.of("UTC")), ZonedDateTime.of(2001, 2, 3, 9, 35, 21, 123457000, ZoneId.of("UTC"))})
);
    }
}
