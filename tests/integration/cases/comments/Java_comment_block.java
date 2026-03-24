import java.util.Map;
class Check {
    public static void check() {
Map.ofEntries(
    /* Server configuration */
    Map.entry("host", "localhost"),  /* default host */
    Map.entry("port", 8080),
    /* Enable debug mode */
    Map.entry("debug", true)
)
    }
}
