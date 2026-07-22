import java.util.Map;
class Main {
    public static void main() {
var my_data = new Object[]{
    Map.ofEntries(Map.entry("present", 1)),
    Map.ofEntries(Map.entry("missing", 2), Map.entry("present", 3))
};
my_data = new Object[]{
    Map.ofEntries(Map.entry("present", 1)),
    Map.ofEntries(Map.entry("missing", 2), Map.entry("present", 3))
};
    }
}
