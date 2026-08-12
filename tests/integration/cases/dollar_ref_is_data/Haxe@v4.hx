class Fixture_dollar_ref_is_data_Haxe {
    public static function main() {
        final my_data = ([
            "value" => (["$ref" => "foo"] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
