import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", new int[]{1, 2, 3}),  // inline a
    Map.entry("b", 2)  // inline b
);
    }
}
