class Fixture_multiline_string_nested_Haxe_type_hints_always {
    public static function main() {
        final my_data:Map<String, Dynamic> = ([
            "outer" => ([(["nested first line\n  indented\n\nnested last line\n"] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
