import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("users", new Object[]{Map.ofEntries(Map.entry("name", "Bob"), Map.entry("tags", new String[]{"admin", "user"})), Map.ofEntries(Map.entry("name", "Carol"), Map.entry("tags", new String[]{"guest"}))})
);
    }
}
