import java.util.Map;
record Record2(int x) {}
record Record1(java.util.ArrayList values, boolean flag) {}
record Record3(String y) {}
record Record0(Record1 first, Record1 second) {}
class Main {
    public static void main() {
var my_data = new Record0(
    new Record1(
        new java.util.ArrayList<>(java.util.Arrays.asList(
            Map.entry("item", new Record2(
                1
            ))
        )),
        true
    ),
    new Record1(
        new java.util.ArrayList<>(java.util.Arrays.asList(
            Map.entry("item", new Record3(
                "s"
            ))
        )),
        false
    )
);
    }
}
