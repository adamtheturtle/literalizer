record Record1(boolean[] k) {}
record Record0(Object[] h) {}
class Main {
    public static void main() {
var my_data = new Record0(
    new Object[]{
        1,
        "a",
        new Object[]{
            2,
            "b"
        },
        new Record1(
            new boolean[]{
                true
            }
        )
    }
);
    }
}
