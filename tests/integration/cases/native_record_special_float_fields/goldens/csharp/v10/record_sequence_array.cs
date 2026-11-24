record Record0(double Positive, double Negative, double NanValue, double Finite);
class Check {
    public static void Main() {
var my_data = new Record0(
    double.PositiveInfinity,
    double.NegativeInfinity,
    double.NaN,
    1.5
);
    _ = my_data;
    }
}
