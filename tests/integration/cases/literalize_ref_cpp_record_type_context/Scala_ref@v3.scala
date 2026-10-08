object Fixture_literalize_ref_cpp_record_type_context_Scala_ref {
case class Record1(x: String)
case class Record2(x: Int)
case class Record0(direct: Record1, bound: Record2)
val first = Record2(
    x = 1,
)
val my_data = Record0(
    direct = Record1(
        x = "s",
    ),
    bound = first,
)
}
