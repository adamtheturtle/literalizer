import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("key", "value \" # not a comment")  // real
);
    }
}
