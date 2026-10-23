import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a_b", 01),
    Map.entry("a-b", 02),
    Map.entry("averyveryverylongkeynamethatgoesonandonandon", 03),
    Map.entry("averyveryverylongkeynamethatgoesonandmore", 04)
);
    }
}
