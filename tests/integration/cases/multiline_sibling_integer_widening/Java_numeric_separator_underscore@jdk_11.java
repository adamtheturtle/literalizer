import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", new long[]{1L}),
    Map.entry("b", new long[]{1_099_511_627_776L})
);
    }
}
