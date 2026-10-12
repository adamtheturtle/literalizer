import java.util.Map;
class Main {
    public static void main() {
var std = Map.ofEntries(
    Map.entry("a", 1)
);
var arena = Map.ofEntries(
    Map.entry("a", 1)
);
var allocator = Map.ofEntries(
    Map.entry("a", 1)
);
var my_data = new Object[]{
    std,
    arena,
    allocator
};
    }
}
