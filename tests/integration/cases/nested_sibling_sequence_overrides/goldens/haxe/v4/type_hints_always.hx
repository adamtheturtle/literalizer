class Fixture_nested_sibling_sequence_overrides_Haxe_type_hints_always {
    public static function main() {
        final my_data:Map<String, Dynamic> = ([
            "a" => ([([1] : Array<Dynamic>), ([2] : Array<Dynamic>)] : Array<Dynamic>),
            "b" => ([(["x"] : Array<Dynamic>), (["y"] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
