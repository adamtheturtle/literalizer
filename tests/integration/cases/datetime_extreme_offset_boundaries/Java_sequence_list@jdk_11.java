import java.time.Instant;
import java.util.List;
class Main {
    public static void main() {
var my_data = List.of(
    Instant.parse("2020-06-16T11:59:00+00:00"),
    Instant.parse("2020-06-15T12:00:00-18:00"),
    Instant.parse("2020-06-15T12:00:00+18:00"),
    Instant.parse("2020-06-14T12:01:00+00:00")
);
    }
}
