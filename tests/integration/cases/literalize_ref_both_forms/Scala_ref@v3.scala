object Fixture_literalize_ref_both_forms_Scala_ref {
var sharedValues = List[Int](
    1,
    2,
)
var my_data = Map[String, List[Int]](
    "a" -> sharedValues,
)
my_data = Map[String, List[Int]](
    "a" -> sharedValues,
)
}
