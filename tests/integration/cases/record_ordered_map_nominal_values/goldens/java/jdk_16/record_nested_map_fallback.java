import java.util.Map;
record Record1(int x) {}
record Record0(java.util.ArrayList values, boolean flag) {}
class Main {
    public static void main() {
var my_data = new Record0(
    new java.util.ArrayList<>(java.util.Arrays.asList(
        Map.entry("first", new Record1(
            1
        )),
        Map.entry("second", new Record1(
            2
        ))
    )),
    true
);
    }
}
