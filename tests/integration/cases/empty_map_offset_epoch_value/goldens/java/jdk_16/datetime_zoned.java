import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Map;
class Main {
    public static void main() {
var my_data = new Object[]{
    Map.ofEntries(Map.entry("timestamp", ZonedDateTime.of(2040, 1, 1, 3, 0, 0, 0, ZoneId.of("+03:00")))),
    Map.ofEntries()
};
    }
}
