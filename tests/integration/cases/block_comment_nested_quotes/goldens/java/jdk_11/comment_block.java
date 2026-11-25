import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    /* "{-" and '{-' stay readable */
    /* balanced {- nested -} and trailing -} stay readable */
    Map.entry("x", 1)
);
    }
}
