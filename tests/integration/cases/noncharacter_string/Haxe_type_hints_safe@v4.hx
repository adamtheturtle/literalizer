class Fixture_noncharacter_string_Haxe_type_hints_safe {
    public static function main() {
        final my_data = ([
            "fffe" => "￾",
            "ffff" => "￿",
        ] : Map<String, Dynamic>);
    }
}
