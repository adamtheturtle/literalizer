import java.time.LocalDate;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", Map.ofEntries(Map.entry("k", LocalDate.of(2020, 1, 1)))),
    Map.entry("b", Map.ofEntries(Map.entry("k", "string")))
);
    }
}
