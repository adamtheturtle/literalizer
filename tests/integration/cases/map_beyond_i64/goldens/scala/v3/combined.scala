object Fixture_map_beyond_i64_Scala_combined {
var my_data = Map[String, BigInt](
    "a" -> BigInt("9223372036854775807"),
    "b" -> BigInt("9223372036854775808"),
)
my_data = Map[String, BigInt](
    "a" -> BigInt("9223372036854775807"),
    "b" -> BigInt("9223372036854775808"),
)
}
