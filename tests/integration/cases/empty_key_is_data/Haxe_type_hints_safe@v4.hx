class Fixture_empty_key_is_data_Haxe_type_hints_safe {
    public static function main() {
        final my_data = ([
            (["" => "external_value"] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
