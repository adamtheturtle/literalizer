import java.util.Map;
import java.math.BigInteger;
class Main {
    public static void main() {
var my_data = Map.ofEntries(
    Map.entry("a", new BigInteger("9223372036854775807")),
    Map.entry("b", new BigInteger("9223372036854775808"))
);
my_data = Map.ofEntries(
    Map.entry("a", new BigInteger("9223372036854775807")),
    Map.entry("b", new BigInteger("9223372036854775808"))
);
    }
}
