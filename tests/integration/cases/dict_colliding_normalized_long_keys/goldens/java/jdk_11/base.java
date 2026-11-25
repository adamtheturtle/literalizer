import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a_b", 1),
    Map.entry("a-b", 2),
    Map.entry("averyveryverylongkeynamethatgoesonandonandon", 3),
    Map.entry("averyveryverylongkeynamethatgoesonandmore", 4)
);
    }
}
