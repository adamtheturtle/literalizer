import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("double", "a b"),
    Map.entry("single", "c d"),
    Map.entry("both", "e f g"),
    Map.entry("continued", "hi"),
    Map.entry("escaped backslash", "j\\ k")
);
    }
}
