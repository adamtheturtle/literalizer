import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    // before
    Map.entry("answer", 42),  // inline
    Map.entry("plain", "ok")
    // trailing
);
    }
}
