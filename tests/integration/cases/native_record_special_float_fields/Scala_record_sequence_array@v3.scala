object Fixture_native_record_special_float_fields_Scala_record_sequence_array {
case class Record0(positive: Double, negative: Double, nan_value: Double, finite: Double)
val my_data = Record0(
    positive = Double.PositiveInfinity,
    negative = Double.NegativeInfinity,
    nan_value = Double.NaN,
    finite = 1.5,
)
}
