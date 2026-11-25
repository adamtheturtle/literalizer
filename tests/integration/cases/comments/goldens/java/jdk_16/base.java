import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    // Server configuration
    Map.entry("host", "localhost"),  // default host
    Map.entry("port", 8080),
    // Enable debug mode
    Map.entry("debug", true)
);
    }
}
