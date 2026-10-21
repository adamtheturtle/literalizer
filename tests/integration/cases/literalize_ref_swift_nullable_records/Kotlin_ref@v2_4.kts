data class Record1(val x: Int, val y: Any?)
data class Record2(val x: Any?, val y: Any?)
data class Record3(val x: Int, val y: Int)
data class Record0(val nullable: Record1, val null_fields: Record2, val plain: Record3)
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
