import java.util.Map;
record Record1(int count, int rate) {}
record Record2(int retries, int timeout) {}
record Record0(Record1 metrics, Record2 flags) {}
class Main {
    public static void main() {
var my_data = new Record0(
    new Record1(
        100,
        50
    ),
    new Record2(
        3,
        30
    )
);
    }
}
