class Fixture_literalize_ref_rust_repeated_nested_Haxe_ref {
    public static function main() {
        final shared = ([
            1,
            2,
        ] : Array<Dynamic>);
        final my_data = ([
            (["left" => shared, "right" => shared] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
