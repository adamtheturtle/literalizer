import java.util.Map;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("user_name", 1),
    Map.entry("user.name", 2),
    Map.entry("user-name", 3),
    Map.entry("field_name_that_is_really_quite_long_one", 4),
    Map.entry("field_name_that_is_really_quite_long_two", 5)
);
my_data = Map.ofEntries(
    Map.entry("user_name", 1),
    Map.entry("user.name", 2),
    Map.entry("user-name", 3),
    Map.entry("field_name_that_is_really_quite_long_one", 4),
    Map.entry("field_name_that_is_really_quite_long_two", 5)
);
    }
}
