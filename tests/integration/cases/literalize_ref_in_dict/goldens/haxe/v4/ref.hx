class Fixture_literalize_ref_in_dict_Haxe_ref {
    public static function main() {
        final myVar = 1;
        final my_data = ([
            "key" => myVar,
        ] : Map<String, Dynamic>);
    }
}
