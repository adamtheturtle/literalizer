import java.util.Map;
record Record1(String name, int age) {}
record Record0(int id, Record1 owner) {}
class Main {
    public static void main() {
var my_data = new Record0(
    1,
    new Record1(
        "Alice",
        30
    )
);
    }
}
