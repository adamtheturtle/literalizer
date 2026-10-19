class Fixture_literalize_ref_nested_null_Haxe_ref {
    public static function main() {
        final myNull = null;
        final my_data = ([
            myNull,
            null,
        ] : Array<Dynamic>);
    }
}
