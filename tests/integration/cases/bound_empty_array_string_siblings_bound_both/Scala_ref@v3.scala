object Fixture_bound_empty_array_string_siblings_bound_both_Scala_ref {
var shared = List[String]()
var second = List[String](
    "one",
    "two",
)
var my_data = List[List[String]](
    shared,
    second,
)
my_data = List[List[String]](
    shared,
    second,
)
}
