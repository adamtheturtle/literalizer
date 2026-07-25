import java.util.Map;
record Record0(int id, String label, boolean enabled, int[] related_ids) {}
class Main {
    public static void main() {
var my_data = new Record0(
    1,
    "She said \"hello\", then waved",
    false,
    new int[]{
        1,
        2,
        3
    }
);
    }
}
