data class Record0(val positive: Double, val negative: Double, val nan_value: Double, val finite: Double)
val my_data = Record0(
    positive = Double.POSITIVE_INFINITY,
    negative = Double.NEGATIVE_INFINITY,
    nan_value = Double.NaN,
    finite = 1.5,
)
