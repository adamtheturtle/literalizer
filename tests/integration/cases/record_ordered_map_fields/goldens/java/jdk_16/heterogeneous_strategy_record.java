import java.util.Map;
record Record0(java.util.ArrayList numbers, java.util.ArrayList words, java.util.ArrayList nested, java.util.ArrayList empty, boolean flag, java.util.ArrayList nested_maps, java.util.ArrayList empty_nested_maps) {}
class Main {
    public static void main() {
var my_data = new Record0(
    new java.util.ArrayList<>(java.util.Arrays.asList(
        Map.entry("first", 1)
    )),
    new java.util.ArrayList<>(java.util.Arrays.asList(
        Map.entry("first", "s")
    )),
    new java.util.ArrayList<>(java.util.Arrays.asList(
        Map.entry("first", new int[]{
            1,
            2
        })
    )),
    new java.util.ArrayList<>(java.util.Arrays.asList()),
    true,
    new java.util.ArrayList<>(java.util.Arrays.asList(
        Map.entry("first", new java.util.ArrayList<>(java.util.Arrays.asList(
            Map.entry("nested", 1)
        )))
    )),
    new java.util.ArrayList<>(java.util.Arrays.asList(
        Map.entry("first", new java.util.ArrayList<>(java.util.Arrays.asList()))
    ))
);
    }
}
