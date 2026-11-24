record Record1(int id, String label) {}
record Record0(String name, Record1[] items) {}
class Main {
    public static void main() {
var my_data = new Record0(
    "box",
    new Record1[]{
        new Record1(
            1,
            "first"
        ),
        new Record1(
            2,
            "second"
        )
    }
);
    }
}
