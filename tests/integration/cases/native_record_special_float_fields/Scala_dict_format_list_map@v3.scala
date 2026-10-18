import scala.collection.immutable.ListMap
object Fixture_native_record_special_float_fields_Scala_dict_format_list_map {
val my_data = ListMap[String, Double](
    "positive" -> Double.PositiveInfinity,
    "negative" -> Double.NegativeInfinity,
    "nan_value" -> Double.NaN,
    "finite" -> 1.5,
)
}
