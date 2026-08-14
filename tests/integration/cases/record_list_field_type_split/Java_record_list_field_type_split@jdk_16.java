import java.util.Map;
record Record1(String kind, boolean urgent) {}
record Record0(Record1[] entries) {}
record Record3(String error) {}
record Record2(Record3[] entries) {}
class Main {
    public static void main() {
var my_data = new java.util.ArrayList<>(java.util.Arrays.asList(
    Map.entry("left", new Record0(new Record1[]{new Record1("add", true)})),
    Map.entry("right", new Record2(new Record3[]{new Record3("not_found")}))
));
    }
}
