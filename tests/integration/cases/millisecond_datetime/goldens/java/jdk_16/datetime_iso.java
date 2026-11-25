import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("half", "1979-05-27T07:32:00.500000"),
    Map.entry("milli", "1979-05-27T07:32:00.100000"),
    Map.entry("max_milli", "1979-05-27T07:32:00.999000"),
    Map.entry("whole", "1979-05-27T07:32:00")
);
    }
}
