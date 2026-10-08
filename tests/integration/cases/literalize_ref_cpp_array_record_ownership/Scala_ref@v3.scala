object Fixture_literalize_ref_cpp_array_record_ownership_Scala_ref {
case class Record1(values: Array[Int])
case class Record2(nested: Array[Array[Int]])
case class Record0(trivial: Record1, nested: Record2)
val trivial = Record1(
    values = Array[Int](
        1,
        2,
    ),
)
val nested = Record2(
    nested = Array[Array[Int]](
        Array[Int](
            1,
            2,
        ),
        Array[Int](
            3,
            4,
        ),
    ),
)
val my_data = Record0(
    trivial = trivial,
    nested = nested,
)
}
