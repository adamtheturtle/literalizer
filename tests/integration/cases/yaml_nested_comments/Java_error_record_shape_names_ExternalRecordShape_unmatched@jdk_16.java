import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", Map.ofEntries(
        // inner note
        Map.entry("b", 1)  // inline b
    )),
    Map.entry("list", new int[]{
        1,  // first
        2  // second
    })
);
    }
}
