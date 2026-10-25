import java.time.ZoneId;
import java.time.ZonedDateTime;
class Main {
static Object consume(Object arg0) { return null; }
    public static void main() {
consume(ZonedDateTime.of(1901, 12, 13, 20, 45, 51, 0, ZoneId.of("UTC")));
consume(ZonedDateTime.of(2038, 1, 19, 3, 14, 8, 0, ZoneId.of("UTC")));
    }
}
