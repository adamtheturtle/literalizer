import java.time.LocalDate;
import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("date", LocalDate.of(99, 5, 27)),
    Map.entry("naive", -62135551800L),
    Map.entry("recent", 1716804000)
);
    }
}
