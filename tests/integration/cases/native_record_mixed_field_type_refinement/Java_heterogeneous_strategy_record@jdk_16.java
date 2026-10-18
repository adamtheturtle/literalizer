record Record2(int value) {}
record Record1(Object[] items) {}
record Record3(String value) {}
record Record0(Record1 first, Record1 second) {}
class Main {
    public static void main() {
var my_data = new Record0(
    new Record1(
        new Object[]{
            1,
            new Record2(
                2
            )
        }
    ),
    new Record1(
        new Object[]{
            1,
            new Record3(
                "s"
            )
        }
    )
);
    }
}
