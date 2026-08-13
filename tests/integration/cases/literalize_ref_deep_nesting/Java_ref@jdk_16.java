import java.util.Map;
class Main {
    public static void main() {
var deep = new int[][]{
    new int[]{
        1,
        2
    },
    new int[]{
        3,
        4
    }
};
var my_data = Map.ofEntries(
    Map.entry("a", Map.ofEntries(
        Map.entry("b", Map.ofEntries(
            Map.entry("c", deep)
        ))
    ))
);
    }
}
