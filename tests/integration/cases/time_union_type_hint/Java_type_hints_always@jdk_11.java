import java.time.LocalTime;
import java.util.Map;
class Main {
    public static void main() {
Map<String, Object[]> my_data = Map.ofEntries(
    Map.entry("mixed", new LocalTime[][]{new LocalTime[]{LocalTime.of(9, 30)}, new LocalTime[]{}})
);
    }
}
