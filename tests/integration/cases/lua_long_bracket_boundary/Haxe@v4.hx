class Fixture_lua_long_bracket_boundary_Haxe {
    public static function main() {
        final my_data = ([
            "]",
            "a]",
            "a]=",
            "a]b",
        ] : Array<Dynamic>);
    }
}
