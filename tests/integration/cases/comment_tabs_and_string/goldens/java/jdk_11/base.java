import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    // before	line
    Map.entry("value", "left\tright")  // inline	line
    // after	line
);
    }
}
