import java.util.Map;
import java.util.Set;
class Check {
    Object x = Map.ofEntries(
    Map.entry("users", new Object[]{Map.ofEntries(Map.entry("name", "Bob"), Map.entry("tags", new Object[]{"admin", "user"})), Map.ofEntries(Map.entry("name", "Carol"), Map.entry("tags", new Object[]{"guest"}))})
);
}
