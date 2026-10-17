class Fixture_literalize_ref_escaped_nested_dict_Haxe_ref {
    public static function main() {
        final existing = 1;
        final my_data = ([
            "nested" => ([0, existing] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
