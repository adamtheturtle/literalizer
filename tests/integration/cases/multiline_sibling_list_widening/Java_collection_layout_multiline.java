import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("sibling_lists", Map.ofEntries(
        Map.entry("numbers", new Object[]{
            1,
            2
        }),
        Map.entry("strings", new Object[]{
            "x",
            "y"
        })
    )),
    Map.entry("ref_marker_present", new String[]{
        "$keep",
        "z"
    })
);
    }
}
