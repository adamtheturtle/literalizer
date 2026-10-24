class Fixture_opt_in_record_example_Haxe_type_hints_safe {
    public static function main() {
        final my_data = ([
            "name" => "Ada",
            "active" => true,
            "scores" => ([1, 2, 3] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
