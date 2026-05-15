import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("id", 1),
    Map.entry("description", "She said \"hello\", then waved"),
    Map.entry("is_done", false),
    Map.entry("blocks", new int[]{1, 2, 3})
);
    }
}
