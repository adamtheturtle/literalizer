class Fixture_literalize_ref_rust_repeated_array_owned_Haxe_ref {
    public static function main() {
        final shared = ([
            (["value" => 1] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
        final my_data = ([
            shared,
            shared,
        ] : Array<Dynamic>);
    }
}
