import java.time.LocalTime;
import java.time.Instant;
class Main {
static Object process(Object... args) { return null; }
    public static void main() {
process(LocalTime.of(9, 30));
process(Instant.parse("2024-01-15T00:00:00+00:00"));
process(1);
    }
}
