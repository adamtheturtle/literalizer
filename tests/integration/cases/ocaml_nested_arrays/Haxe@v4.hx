class Fixture_ocaml_nested_arrays_Haxe {
    public static function main() {
        final my_data = ([
            ([([1] : Array<Dynamic>)] : Array<Dynamic>),
            ([([] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
