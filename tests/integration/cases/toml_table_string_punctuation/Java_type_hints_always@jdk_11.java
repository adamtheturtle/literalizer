import java.util.Map;
class Main {
    public static void main() {
Map<String, String> my_data = Map.ofEntries(
    Map.entry("comma_hash", "a,#b"),
    Map.entry("comma_space_hash", "trail, # comment"),
    Map.entry("escaped_quote", "quote \" and , #"),
    Map.entry("next_line", "xy"),
    Map.entry("line_separator", "x y"),
    Map.entry("paragraph_separator", "x y")
);
    }
}
