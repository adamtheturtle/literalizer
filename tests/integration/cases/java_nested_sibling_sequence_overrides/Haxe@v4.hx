class Fixture_java_nested_sibling_sequence_overrides_Haxe {
    public static function main() {
        final my_data = ([
            "a" => ([([1] : Array<Dynamic>), ([2] : Array<Dynamic>)] : Array<Dynamic>),
            "b" => ([(["x"] : Array<Dynamic>), (["y"] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
