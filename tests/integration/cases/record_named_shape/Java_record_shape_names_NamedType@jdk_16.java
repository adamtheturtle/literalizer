import java.util.Map;
record NamedType(int id, String label, boolean enabled, int[] related_ids) {}
class Main {
    public static void main() {
var my_data = new Object[]{
    new NamedType(100, "first item", false, new int[]{102, 103}),
    new NamedType(101, "second item", true, new int[]{100})
};
    }
}
