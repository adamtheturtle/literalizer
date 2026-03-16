import java.util.Map;
import java.util.Set;
class Check {
    public static void check() {
var my_data = Map.ofEntries(
    // Server configuration
    Map.entry("host", "localhost"),  // default host
    Map.entry("port", 8080),
    // Enable debug mode
    Map.entry("debug", true)
);
    }
}
