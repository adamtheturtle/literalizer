import java.time.LocalDate;
import java.util.Map;
record Record0(String s, int i, double f, boolean b, Object n, LocalDate d, int dt, String by) {}
class Main {
    public static void main() {
var my_data = new Record0(
    "string",
    1,
    1.5,
    true,
    null,
    LocalDate.of(2024, 1, 15),
    1705320000,
    "48656c6c6f"
);
    }
}
