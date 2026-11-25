class Fixture_dict_colliding_normalized_long_keys_Haxe_integer_format_hex {
    public static function main() {
        final my_data = ([
            "a_b" => 0x1,
            "a-b" => 0x2,
            "averyveryverylongkeynamethatgoesonandonandon" => 0x3,
            "averyveryverylongkeynamethatgoesonandmore" => 0x4,
        ] : Map<String, Dynamic>);
    }
}
