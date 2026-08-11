class Fixture_dict_colliding_normalized_long_keys_Haxe {
    public static function main() {
        final my_data = ([
            "a_b" => 1,
            "a-b" => 2,
            "averyveryverylongkeynamethatgoesonandonandon" => 3,
            "averyveryverylongkeynamethatgoesonandmore" => 4,
        ] : Map<String, Dynamic>);
    }
}
