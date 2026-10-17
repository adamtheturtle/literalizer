import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("cr", "a\rb"),
    Map.entry("crlf", "a\r\nb"),
    Map.entry("lf", "a\nb")
);
    }
}
