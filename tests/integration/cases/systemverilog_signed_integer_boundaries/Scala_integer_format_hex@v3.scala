object Fixture_systemverilog_signed_integer_boundaries_Scala_integer_format_hex {
val my_data = Map[String, Long](
    "i32_below" -> -0x80000001L,
    "i32_minimum" -> -0x80000000,
    "i32_above" -> -0x7fffffff,
    "i32_maximum" -> 0x7fffffff,
    "i32_over" -> 0x80000000L,
    "i64_minimum" -> -0x8000000000000000L,
    "i64_maximum" -> 0x7fffffffffffffffL,
)
}
