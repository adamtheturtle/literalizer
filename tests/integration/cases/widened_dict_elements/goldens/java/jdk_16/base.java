import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", new Object[]{Map.ofEntries(), Map.ofEntries(Map.entry("x", 1))}),
    Map.entry("b", new Object[]{new int[]{}, new int[]{1}})
);
    }
}
