import java.util.Map;
import java.util.List;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("alpha", List.of(2, List.of())),
    Map.entry("beta", List.of(5, List.of("x")))
);
    }
}
