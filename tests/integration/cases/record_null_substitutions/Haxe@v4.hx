class Fixture_record_null_substitutions_Haxe {
    public static function main() {
        final my_data = ([
            (["missing" => -1, "present" => 1] : Map<String, Dynamic>),
            (["missing" => 2, "present" => 3] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
