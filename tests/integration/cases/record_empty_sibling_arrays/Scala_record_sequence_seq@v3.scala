object Fixture_record_empty_sibling_arrays_Scala_record_sequence_seq {
case class Record1(item: Int)
case class Record2(item: Any)
case class Record0(integers: Seq[Any], nulls: Seq[Any], nested: Seq[Any], reversed: Seq[Any])
val my_data = Record0(
    integers = Seq(
        Seq(),
        Seq(
            Record1(
                item = 1,
            ),
        ),
    ),
    nulls = Seq(
        Seq(),
        Seq(
            Record2(
                item = null,
            ),
        ),
    ),
    nested = Seq(
        Seq(
            Seq(),
            Seq(
                Record1(
                    item = 2,
                ),
            ),
        ),
        Seq(
            Seq(
                Record1(
                    item = 3,
                ),
            ),
            Seq(),
        ),
    ),
    reversed = Seq(
        Seq(
            Record1(
                item = 4,
            ),
        ),
        Seq(),
    ),
)
}
