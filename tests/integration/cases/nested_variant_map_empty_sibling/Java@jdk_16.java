import java.util.Map;
class Main {
    public static void main() {
var my_data = new Object[]{
    Map.ofEntries(Map.entry("nested", Map.ofEntries(Map.entry("count", 1), Map.entry("name", "value")))),
    Map.ofEntries()
};
    }
}
