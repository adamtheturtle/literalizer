class Fixture_dict_colliding_cobol_keys_Haxe_combined {
    public static function main() {
        var my_data = ([
            "user_name" => 1,
            "user.name" => 2,
            "user-name" => 3,
            "field_name_that_is_really_quite_long_one" => 4,
            "field_name_that_is_really_quite_long_two" => 5,
        ] : Map<String, Dynamic>);
        my_data = ([
            "user_name" => 1,
            "user.name" => 2,
            "user-name" => 3,
            "field_name_that_is_really_quite_long_one" => 4,
            "field_name_that_is_really_quite_long_two" => 5,
        ] : Map<String, Dynamic>);
    }
}
