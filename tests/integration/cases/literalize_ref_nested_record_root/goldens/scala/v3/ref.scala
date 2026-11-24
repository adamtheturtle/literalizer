object Fixture_literalize_ref_nested_record_root_Scala_ref {
case class Record1(value: Int)
case class Record0(child: Record1)
val first = Record0(
    child = Record1(
        value = 1,
    ),
)
val my_data = first
}
