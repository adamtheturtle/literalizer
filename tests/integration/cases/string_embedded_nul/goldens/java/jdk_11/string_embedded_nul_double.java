import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("x", "\000"),
    Map.entry("y", "\0001")
);
    }
}
