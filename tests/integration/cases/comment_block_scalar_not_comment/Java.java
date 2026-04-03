import java.util.Map;
class Check {
    public static void check() {
var my_data = Map.ofEntries(
    Map.entry("description", "# not a comment\n"),
    Map.entry("name", "foo")
);
    }
}
