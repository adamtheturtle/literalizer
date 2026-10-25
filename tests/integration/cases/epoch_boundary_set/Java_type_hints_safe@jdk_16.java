import java.time.Instant;
import java.util.Set;
class Main {
    public static void main() {
var my_data = Set.of(
    Instant.parse("1901-12-13T20:45:51Z"),
    Instant.parse("1901-12-13T20:45:52Z"),
    Instant.parse("2038-01-19T03:14:07Z"),
    Instant.parse("2038-01-19T03:14:08Z")
);
    }
}
