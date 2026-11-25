import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a-b", 1),
    Map.entry("two words", 2),
    Map.entry("she said \"hi\"", 3),
    Map.entry("", 4),
    Map.entry("valid_key", 5)
);
    }
}
