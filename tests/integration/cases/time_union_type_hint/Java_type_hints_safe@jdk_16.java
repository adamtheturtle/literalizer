import java.time.LocalTime;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("mixed", new LocalTime[][]{new LocalTime[]{LocalTime.of(9, 30)}, new LocalTime[]{}})
);
    }
}
