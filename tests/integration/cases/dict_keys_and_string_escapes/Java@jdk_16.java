import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("plain", new int[]{1, 2}),
    Map.entry("with-dash", "a\nb")
);
    }
}
