import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", new Object[]{new Object[]{1}, new Object[]{2}}),
    Map.entry("b", new Object[]{new Object[]{"x"}, new Object[]{"y"}})
);
    }
}
