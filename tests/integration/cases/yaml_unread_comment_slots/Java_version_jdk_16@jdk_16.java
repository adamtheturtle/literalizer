import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("flow", new int[]{
        1,
        // After the first element.
        2
    }),
    // Between the key and its value.
    Map.entry("gap", 3),
    // On the block scalar header.
    Map.entry("block", "Text.\n"),
    Map.entry("nested", new int[]{
        1,
        1
        // On the nested alias.
    }),
    Map.entry("anchored", 4),
    Map.entry("alias", 4)
    // On the alias.
);
    }
}
