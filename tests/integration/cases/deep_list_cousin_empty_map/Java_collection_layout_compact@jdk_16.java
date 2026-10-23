import java.util.Map;
class Main {
    public static void main() {
var my_data = new Object[]{
    Map.ofEntries(Map.entry("items", new Object[]{Map.ofEntries(Map.entry("inner", Map.ofEntries(Map.entry("x", 1)))), Map.ofEntries(Map.entry("inner", Map.ofEntries()))})),
    Map.ofEntries(Map.entry("items", new Object[]{Map.ofEntries(Map.entry("inner", Map.ofEntries(Map.entry("x", 2)))), Map.ofEntries(Map.entry("inner", Map.ofEntries()))}))
};
    }
}
