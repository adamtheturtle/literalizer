import java.time.LocalDate;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("date", LocalDate.of(99, 5, 27)),
    Map.entry("naive", "0001-01-01T12:30:00"),
    Map.entry("recent", "2024-05-27T10:00:00")
);
    }
}
