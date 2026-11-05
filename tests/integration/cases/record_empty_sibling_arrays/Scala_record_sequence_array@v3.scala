object Fixture_record_empty_sibling_arrays_Scala_record_sequence_array {
case class Record1(item: Int)
case class Record2(item: Any)
case class Record0(integers: Array[Any], nulls: Array[Any], nested: Array[Any], reversed: Array[Any])
val my_data = Record0(
    integers = Array[Any](
        Array.empty[Any],
        Array(
            Record1(
                item = 1,
            ),
        ),
    ),
    nulls = Array[Any](
        Array.empty[Any],
        Array(
            Record2(
                item = null,
            ),
        ),
    ),
    nested = Array(
        Array[Any](
            Array.empty[Any],
            Array(
                Record1(
                    item = 2,
                ),
            ),
        ),
        Array[Any](
            Array(
                Record1(
                    item = 3,
                ),
            ),
            Array.empty[Any],
        ),
    ),
    reversed = Array[Any](
        Array(
            Record1(
                item = 4,
            ),
        ),
        Array.empty[Any],
    ),
)
}
