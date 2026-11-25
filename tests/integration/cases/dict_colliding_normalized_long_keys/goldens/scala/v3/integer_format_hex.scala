object Fixture_dict_colliding_normalized_long_keys_Scala_integer_format_hex {
val my_data = Map[String, Int](
    "a_b" -> 0x1,
    "a-b" -> 0x2,
    "averyveryverylongkeynamethatgoesonandonandon" -> 0x3,
    "averyveryverylongkeynamethatgoesonandmore" -> 0x4,
)
}
