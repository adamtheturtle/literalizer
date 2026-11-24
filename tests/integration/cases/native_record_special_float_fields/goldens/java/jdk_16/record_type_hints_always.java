record Record0(double positive, double negative, double nan_value, double finite) {}
class Main {
    public static void main() {
Record0 my_data = new Record0(
    Double.POSITIVE_INFINITY,
    Double.NEGATIVE_INFINITY,
    Double.NaN,
    1.5
);
    }
}
