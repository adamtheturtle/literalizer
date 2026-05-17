class Fixture_dict_with_control_char_keys_Haxe {
    public static function main() {
        final my_data = ([
            "key\nwith\nnewlines" => "value1",
            "key\twith\ttabs" => "value2",
            "" => "value3",
        ] : Map<String, Dynamic>);
    }
}
