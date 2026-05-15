import java.util.Map;
record Record1(int[] numbers, String[] strings) {}
record Record0(java.util.ArrayList omap_value, Record1 sibling_lists, String[] ref_marker_present) {}
class Main {
    public static void main() {
var my_data = new Record0(
    new java.util.ArrayList<>(java.util.Arrays.asList(
        Map.entry("first", 1)
    )),
    new Record1(
        new int[]{
            1,
            2
        },
        new String[]{
            "x",
            "y"
        }
    ),
    new String[]{
        "$keep",
        "z"
    }
);
    }
}
