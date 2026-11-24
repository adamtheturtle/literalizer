import java.time.LocalTime;
import java.util.Map;
class Main {
    public static void main() {
Map<String, LocalTime> my_data = Map.ofEntries(
    Map.entry("morning", LocalTime.of(9, 30)),
    Map.entry("afternoon", LocalTime.of(14, 15)),
    Map.entry("evening", LocalTime.of(23, 59, 59))
);
    }
}
