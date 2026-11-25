import java.math.BigInteger;
record Record0(int quantity, BigInteger big, double ratio, String label, boolean ok) {}
class Main {
    public static void main() {
Record0 my_data = new Record0(
    1000000,
    new BigInteger("18446744073709551615"),
    2.5,
    "tag",
    true
);
    }
}
