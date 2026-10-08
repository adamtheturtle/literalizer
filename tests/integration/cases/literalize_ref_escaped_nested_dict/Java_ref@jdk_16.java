import java.util.Map;
class Main {
    public static void main() {
var existing = 1;
var my_data = Map.ofEntries(
    Map.entry("nested", new int[]{0, existing})
);
    }
}
