object Fixture_literalize_ref_mutable_record_arrays_both_forms_Scala_ref {
case class Record0(id: Int)
var shared = List(
    Record0(id = 1),
)
var second = List(
    Record0(id = 2),
)
var my_data = List(
    shared,
    second,
)
my_data = List(
    shared,
    second,
)
}
