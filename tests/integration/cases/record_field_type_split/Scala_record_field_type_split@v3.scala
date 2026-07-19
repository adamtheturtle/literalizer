object Fixture_record_field_type_split_Scala_record_field_type_split {
case class Record1(status: Int)
case class Record2(status: String)
case class Record4(kind: String, urgent: Boolean)
case class Record3(inner: Record4)
case class Record6(error: String)
case class Record5(inner: Record6)
case class Record7(holder: Record1)
case class Record8(holder: Record2)
case class Record9(nums: List[Long])
case class Record0(plain: Record1, other: Record2, nested_a: Record3, nested_b: Record5, wrap_a: Record7, wrap_b: Record8, wide: Record9)
val my_data = Record0(
    plain = Record1(
        status = 1,
    ),
    other = Record2(
        status = "ready",
    ),
    nested_a = Record3(
        inner = Record4(
            kind = "add",
            urgent = true,
        ),
    ),
    nested_b = Record5(
        inner = Record6(
            error = "not_found",
        ),
    ),
    wrap_a = Record7(
        holder = Record1(
            status = 2,
        ),
    ),
    wrap_b = Record8(
        holder = Record2(
            status = "word",
        ),
    ),
    wide = Record9(
        nums = List[Long](
            1,
            1099511627776L,
        ),
    ),
)
}
