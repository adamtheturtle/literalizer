import java.util.Map;
record Record0(String title, String[] tags, int priority) {}
class Main {
    public static void main() {
var my_data = new Record0(
    "report",
    new String[]{
        "draft",
        "urgent",
        "review"
    },
    2
);
    }
}
