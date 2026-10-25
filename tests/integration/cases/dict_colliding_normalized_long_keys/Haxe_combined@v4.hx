class Fixture_dict_colliding_normalized_long_keys_Haxe_combined {
    public static function main() {
        var my_data = ([
            "a_b" => 1,
            "a-b" => 2,
            "averyveryverylongkeynamethatgoesonandonandon" => 3,
            "averyveryverylongkeynamethatgoesonandmore" => 4,
        ] : Map<String, Dynamic>);
        my_data = ([
            "a_b" => 1,
            "a-b" => 2,
            "averyveryverylongkeynamethatgoesonandonandon" => 3,
            "averyveryverylongkeynamethatgoesonandmore" => 4,
        ] : Map<String, Dynamic>);
    }
}
