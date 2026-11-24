import java.util.Map;
record Record0(String name, java.util.Map<String, Object> payload) {}
class Main {
    public static void main() {
var my_data = new Record0[]{
    new Record0("one", Map.ofEntries(Map.entry("scalar", 1), Map.entry("items", new int[]{2, 3}))),
    new Record0("two", Map.ofEntries(Map.entry("other", 2)))
};
    }
}
