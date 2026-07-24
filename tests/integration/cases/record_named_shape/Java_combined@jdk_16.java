import java.util.Map;
class Main {
    public static void main() {
var my_data = new Object[]{
    Map.ofEntries(Map.entry("id", 100), Map.entry("label", "first entry"), Map.entry("enabled", false), Map.entry("related_ids", new int[]{102, 103})),
    Map.ofEntries(Map.entry("id", 101), Map.entry("label", "second entry"), Map.entry("enabled", true), Map.entry("related_ids", new int[]{100}))
};
my_data = new Object[]{
    Map.ofEntries(Map.entry("id", 100), Map.entry("label", "first entry"), Map.entry("enabled", false), Map.entry("related_ids", new int[]{102, 103})),
    Map.ofEntries(Map.entry("id", 101), Map.entry("label", "second entry"), Map.entry("enabled", true), Map.entry("related_ids", new int[]{100}))
};
    }
}
