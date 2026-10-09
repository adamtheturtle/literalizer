object Fixture_literalize_ref_both_forms_Scala_ref {
var shared = List[Int](
    1,
    2,
)
var my_data = Map[String, List[Int]](
    "a" -> shared,
)
my_data = Map[String, List[Int]](
    "a" -> shared,
)
}
