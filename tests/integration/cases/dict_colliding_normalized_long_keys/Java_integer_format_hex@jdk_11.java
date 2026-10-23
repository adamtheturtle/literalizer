import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a_b", 0x1),
    Map.entry("a-b", 0x2),
    Map.entry("averyveryverylongkeynamethatgoesonandonandon", 0x3),
    Map.entry("averyveryverylongkeynamethatgoesonandmore", 0x4)
);
    }
}
