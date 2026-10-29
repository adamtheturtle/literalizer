import java.util.Map;
import java.util.Set;
record Record0(String name, java.util.Map<String, Object> payload) {}
class Main {
    public static void main() {
var ZKV = new Record0[]{
    new Record0(
        "ZVal ZKV literalizer record value",
        Map.ofEntries(
            Map.entry("scalar", 1),
            Map.entry("items", Set.of(
                2,
                3
            ))
        )
    ),
    new Record0(
        "two",
        Map.ofEntries(
            Map.entry("other", 2)
        )
    )
};
    }
}
