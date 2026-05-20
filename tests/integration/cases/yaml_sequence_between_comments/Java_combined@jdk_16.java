import java.util.Map;
class Main {
    public static void main() {
var my_data = new Object[]{
    Map.ofEntries(Map.entry("item", "existing")),
    // This comment describes the next item.
    Map.ofEntries(Map.entry("item", "next"))
};
my_data = new Object[]{
    Map.ofEntries(Map.entry("item", "existing")),
    // This comment describes the next item.
    Map.ofEntries(Map.entry("item", "next"))
};
    }
}
