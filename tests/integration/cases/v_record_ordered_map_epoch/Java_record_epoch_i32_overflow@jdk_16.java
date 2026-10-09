import java.util.Map;
record Record0(java.util.ArrayList values, boolean flag, java.util.ArrayList nested_values, java.util.ArrayList list_values) {}
class Main {
    public static void main() {
var my_data = new Record0(
    new java.util.ArrayList<>(java.util.Arrays.asList(
        Map.entry("first", 2208988800L)
    )),
    true,
    new java.util.ArrayList<>(java.util.Arrays.asList(
        Map.entry("first", new java.util.ArrayList<>(java.util.Arrays.asList(
            Map.entry("nested", 2208988800L)
        )))
    )),
    new java.util.ArrayList<>(java.util.Arrays.asList(
        Map.entry("first", new long[]{
            2208988800L
        })
    ))
);
    }
}
