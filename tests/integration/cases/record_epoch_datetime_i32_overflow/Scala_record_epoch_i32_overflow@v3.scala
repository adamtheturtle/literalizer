object Fixture_record_epoch_datetime_i32_overflow_Scala_record_epoch_i32_overflow {
case class Record0(within_i32: Int, beyond_i32: Long)
val my_data = Record0(
    within_i32 = 1705320000,
    beyond_i32 = 4085195400L,
)
}
