class Fixture_dict_with_hyphen_keys_Haxe {
    public static function main() {
        final my_data = ([
            "my-key" => "value1",
            "another-key" => "value2",
            "normal_key" => "value3",
        ] : Map<String, Dynamic>);
    }
}
