import java.util.Map;
record Record1(int a, String b, Object c) {}
record Record0(Record1 outer) {}
class Main {
    public static void main() {
var my_data = new Record0(
    new Record1(
        1,
        "x",
        null
    )
);
    }
}
