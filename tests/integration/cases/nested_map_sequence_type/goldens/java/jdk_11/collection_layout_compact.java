import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", Map.ofEntries(Map.entry("b", new int[]{1, 2, 3})))
);
    }
}
