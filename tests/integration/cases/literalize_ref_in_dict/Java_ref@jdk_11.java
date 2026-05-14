import java.util.Map;
class Main {
    public static void main() {
var myVar = Map.ofEntries(
    Map.entry("_", "_")
);
var my_data = Map.ofEntries(
    Map.entry("key", myVar)
);
    }
}
