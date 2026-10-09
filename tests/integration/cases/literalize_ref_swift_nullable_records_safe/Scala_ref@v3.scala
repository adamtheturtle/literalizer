object Fixture_literalize_ref_swift_nullable_records_safe_Scala_ref {
case class Record1(x: Int, y: Any)
case class Record2(x: Any, y: Any)
case class Record3(x: Int, y: Int)
case class Record0(nullable: Record1, null_fields: Record2, plain: Record3)
val nullable = Record1(
    x = 1,
    y = null,
)
val nullFields = Record2(
    x = null,
    y = null,
)
val plain = Record3(
    x = 1,
    y = 2,
)
val my_data = Record0(
    nullable = nullable,
    null_fields = nullFields,
    plain = plain,
)
}
