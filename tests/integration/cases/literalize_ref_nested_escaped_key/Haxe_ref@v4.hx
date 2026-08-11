class Fixture_literalize_ref_nested_escaped_key_Haxe_ref {
    public static function main() {
        final foo = ([
            "_" => "_",
        ] : Map<String, Dynamic>);
        final my_data = ([
            "items" => ([(["other" => 1] : Map<String, Dynamic>), foo] : Array<Dynamic>),
            "mapping" => (["value" => foo] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
