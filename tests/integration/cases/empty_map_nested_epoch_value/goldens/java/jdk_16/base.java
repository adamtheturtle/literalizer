import java.time.Instant;
import java.util.Map;
class Main {
    public static void main() {
var my_data = new Object[]{
    Map.ofEntries(Map.entry("nested", Map.ofEntries(Map.entry("times", new Object[]{Instant.parse("1900-01-01T00:00:00+00:00")})))),
    Map.ofEntries()
};
    }
}
