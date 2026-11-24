class Fixture_dict_keys_and_string_escapes_Haxe {
    public static function main() {
        final my_data = ([
            "plain" => ([1, 2] : Array<Dynamic>),
            "with-dash" => "a\nb",
        ] : Map<String, Dynamic>);
    }
}
