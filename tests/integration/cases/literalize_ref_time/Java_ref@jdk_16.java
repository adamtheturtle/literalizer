import java.time.LocalTime;
import java.util.Map;
class Main {
    public static void main() {
var myTime = LocalTime.of(1, 2, 3);
var my_data = Map.ofEntries(
    Map.entry("x", myTime)
);
    }
}
