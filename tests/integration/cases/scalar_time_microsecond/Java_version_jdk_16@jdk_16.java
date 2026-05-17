import java.time.LocalTime;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("exact_millisecond", LocalTime.of(9, 30, 15, 123000000)),
    Map.entry("sub_millisecond", LocalTime.of(9, 30, 15, 123456000))
);
    }
}
