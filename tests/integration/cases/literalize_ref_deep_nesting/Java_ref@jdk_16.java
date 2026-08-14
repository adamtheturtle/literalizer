import java.util.Map;
class Main {
    public static void main() {
var deep = new String[][]{
    new String[]{
        "one",
        "two"
    },
    new String[]{
        "three",
        "four"
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
