import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Set;
class Main {
    public static void main() {
var my_data = Set.of(
    ZonedDateTime.of(1901, 12, 13, 20, 45, 51, 0, ZoneId.of("UTC")),
    ZonedDateTime.of(1901, 12, 13, 20, 45, 52, 0, ZoneId.of("UTC")),
    ZonedDateTime.of(2038, 1, 19, 3, 14, 7, 0, ZoneId.of("UTC")),
    ZonedDateTime.of(2038, 1, 19, 3, 14, 8, 0, ZoneId.of("UTC"))
);
    }
}
