import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a_b", 0b1),
    Map.entry("a-b", 0b10),
    Map.entry("averyveryverylongkeynamethatgoesonandonandon", 0b11),
    Map.entry("averyveryverylongkeynamethatgoesonandmore", 0b100)
);
    }
}
