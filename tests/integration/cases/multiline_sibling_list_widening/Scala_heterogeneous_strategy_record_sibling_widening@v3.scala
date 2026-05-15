object Fixture_multiline_sibling_list_widening_Scala_heterogeneous_strategy_record_sibling_widening {
case class Record1(numbers: List[Int], strings: List[String])
case class Record0(omap_value: scala.collection.immutable.ListMap[String, Any], sibling_lists: Record1, ref_marker_present: List[String])
val my_data = Record0(
    omap_value = scala.collection.immutable.ListMap(
        "first" -> 1,
    ),
    sibling_lists = Record1(
        numbers = List[Int](
            1,
            2,
        ),
        strings = List[String](
            "x",
            "y",
        ),
    ),
    ref_marker_present = List[String](
        "$keep",
        "z",
    ),
)
}
