object Fixture_multiline_sibling_list_widening_Scala {
val my_data = Map(
    "omap_value" -> scala.collection.immutable.ListMap("first" -> 1),
    "sibling_lists" -> Map("numbers" -> List(1, 2), "strings" -> List("x", "y")),
    "ref_marker_present" -> List[String]("$keep", "z"),
)
}
