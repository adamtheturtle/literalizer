import java.util.Map;
class Main {
    public static void main() {
var shared = "s";
var my_data = Map.ofEntries(
    Map.entry("value", shared)
);
    }
}
