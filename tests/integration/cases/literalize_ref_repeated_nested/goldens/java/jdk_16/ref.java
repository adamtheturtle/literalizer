import java.util.Map;
class Main {
    public static void main() {
var shared = new int[]{
    1,
    2
};
var my_data = new Object[]{
    Map.ofEntries(Map.entry("left", shared), Map.entry("right", shared))
};
    }
}
