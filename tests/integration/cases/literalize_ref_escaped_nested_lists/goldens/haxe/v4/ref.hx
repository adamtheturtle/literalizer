class Fixture_literalize_ref_escaped_nested_lists_Haxe_ref {
    public static function main() {
        final existing = 1;
        final my_data = ([
            0,
            ([([existing] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
