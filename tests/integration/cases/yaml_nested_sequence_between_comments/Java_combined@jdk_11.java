import java.util.Map;
class Main {
    public static void main() {
var my_data = new Object[]{
    new Object[]{
        Map.ofEntries(Map.entry("item", "existing")),
        "kept"
        // This comment trails the first pair.
    },
    new Object[]{Map.ofEntries(Map.entry("item", "next")), "also kept"},
    // This comment describes the last pair.
    new Object[]{Map.ofEntries(Map.entry("item", "last")), "kept too"}
};
my_data = new Object[]{
    new Object[]{
        Map.ofEntries(Map.entry("item", "existing")),
        "kept"
        // This comment trails the first pair.
    },
    new Object[]{Map.ofEntries(Map.entry("item", "next")), "also kept"},
    // This comment describes the last pair.
    new Object[]{Map.ofEntries(Map.entry("item", "last")), "kept too"}
};
    }
}
