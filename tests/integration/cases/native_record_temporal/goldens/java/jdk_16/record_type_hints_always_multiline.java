import java.time.LocalTime;
import java.time.LocalDate;
import java.time.Instant;
record Record0(LocalDate birthday, LocalTime meeting, Instant event_time) {}
class Main {
    public static void main() {
Record0 my_data = new Record0(
    LocalDate.of(2024, 1, 15),
    LocalTime.of(9, 30),
    Instant.parse("2024-01-15T12:30:00+00:00")
);
    }
}
