using System;
class Check {
static object? capture(object? nan_value = null, object? positive_infinity = null, object? negative_infinity = null, object? finite_value = null, object? date_value = null, object? datetime_value = null, object? text_value = null) => null;
    public static void Main() {
capture(double.NaN, double.PositiveInfinity, double.NegativeInfinity, 1.25, new DateOnly(2024, 1, 15), 1705322096, "[ordinary text]");
    }
}
