class Fixture_literalize_ref_in_list_Haxe_ref {
    public static function main() {
        final valX = ([
            "_" => "_",
        ] : Map<String, Dynamic>);
        final valY = ([
            "_" => "_",
        ] : Map<String, Dynamic>);
        final my_data = ([
            valX,
            valY,
        ] : Array<Dynamic>);
    }
}
