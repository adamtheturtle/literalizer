import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    // A JSONC input case with both comment forms.
    Map.entry("url", "https://example.org/a/*b*/"),  // detail
    // continued
    Map.entry("count", 2)  // trailing line comment
);
    }
}
