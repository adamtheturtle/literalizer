import java.util.Map;
class Main {
    public static void main() {
var my_data = new Object[]{
    Map.ofEntries(Map.entry("id", 100), Map.entry("description", "first task"), Map.entry("is_done", false), Map.entry("blocks", new int[]{102, 103})),
    Map.ofEntries(Map.entry("id", 101), Map.entry("description", "second task"), Map.entry("is_done", true), Map.entry("blocks", new int[]{100}))
};
    }
}
