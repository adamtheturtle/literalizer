import java.util.Map;
import java.util.Set;
class Check {
    public static void check() {
var my_data = Map.ofEntries(
    Map.entry("users", new Object[]{Map.ofEntries(Map.entry("name", "Bob"), Map.entry("tags", new Object[]{"admin", "user"})), Map.ofEntries(Map.entry("name", "Carol"), Map.entry("tags", new Object[]{"guest"}))})
);
    }
}
