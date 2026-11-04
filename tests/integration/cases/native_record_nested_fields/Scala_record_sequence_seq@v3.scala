object Fixture_native_record_nested_fields_Scala_record_sequence_seq {
case class Record1(name: String, active: Boolean)
case class Record2(name: String, score: Double)
case class Record0(owner: Record1, members: Seq[Any])
val my_data = Record0(
    owner = Record1(
        name = "Ada",
        active = false,
    ),
    members = Seq(
        Record2(
            name = "Ada",
            score = 1.5,
        ),
        Record2(
            name = "Bob",
            score = 2.5,
        ),
    ),
)
}
