import java.time.LocalDate;
import java.time.Instant;
class Main {
static Object check(Object... args) { return null; }
    public static void main() {
check(Instant.parse("2024-01-15T10:30:00+00:00"), LocalDate.of(2024, 6, 1));
    }
}
