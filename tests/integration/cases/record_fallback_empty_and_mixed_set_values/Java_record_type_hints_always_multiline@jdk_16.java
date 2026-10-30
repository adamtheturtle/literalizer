import java.util.Map;
import java.util.Set;
record Record0(String name, java.util.Map<String, Object> payload) {}
class Main {
    public static void main() {
Record0[] my_data = new Record0[]{
    new Record0(
        "one",
        Map.ofEntries(
            Map.entry("scalar", 1),
            Map.entry("empty", Set.of()),
            Map.entry("mixed", Set.of(
                2,
                "word"
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
