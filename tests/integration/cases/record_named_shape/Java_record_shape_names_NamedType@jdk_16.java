import java.util.Map;
record NamedType(int id, String description, boolean is_done, int[] blocks) {}
class Main {
    public static void main() {
var my_data = new Object[]{
    new NamedType(100, "first task", false, new int[]{102, 103}),
    new NamedType(101, "second task", true, new int[]{100})
};
    }
}
