class Fixture_multiline_string_nested_Haxe_type_hints_safe {
    public static function main() {
        final my_data = ([
            "outer" => ([(["nested first line\n  indented\n\nnested last line\n"] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
