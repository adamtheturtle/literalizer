object Fixture_csharp_record_ordered_map_epoch_arrays_Scala_record_epoch_i32_overflow {
case class Record0(values: scala.collection.immutable.ListMap[String, Any], flag: Boolean, direct_arrays: List[List[Long]])
val my_data = Record0(
    values = scala.collection.immutable.ListMap(
        "wide" -> List[List[Long]](
            List[Long](
                2208988800L,
            ),
            List[Long](),
        ),
        "narrow" -> List[List[Long]](
            List[Long](
                946684800L,
            ),
        ),
        "negative" -> List[List[Long]](
            List[Long](
                -2208988800L,
            ),
        ),
        "shifted" -> List[List[Long]](
            List[Long](
                2208988800L,
            ),
        ),
        "mixed_width" -> List[List[Long]](
            List[Long](
                946684800L,
            ),
            List[Long](
                2208988800L,
            ),
        ),
        "text" -> "preserve",
    ),
    flag = true,
    direct_arrays = List[List[Long]](
        List[Long](
            2208988800L,
        ),
        List[Long](),
    ),
)
}
