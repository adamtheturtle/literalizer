class Fixture_literalize_ref_repeated_null_and_literal_Haxe_ref {
    public static function main() {
        final value = null;
        final my_data = ([
            value,
            value,
            null,
        ] : Array<Dynamic>);
    }
}
