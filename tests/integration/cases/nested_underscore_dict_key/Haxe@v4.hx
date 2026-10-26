class Fixture_nested_underscore_dict_key_Haxe {
    public static function main() {
        final my_data = ([
            "outer" => ([(["_" => 1] : Map<String, Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
