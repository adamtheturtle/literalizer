import java.time.LocalTime;
import java.util.Map;
import java.util.List;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("times", List.of(LocalTime.of(9, 30), LocalTime.of(17, 45), LocalTime.of(23, 59, 59)))
);
    }
}
