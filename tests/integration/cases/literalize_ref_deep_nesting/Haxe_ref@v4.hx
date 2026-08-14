class Fixture_literalize_ref_deep_nesting_Haxe_ref {
    public static function main() {
        final deep = ([
            ([
                "one",
                "two",
            ] : Array<Dynamic>),
            ([
                "three",
                "four",
            ] : Array<Dynamic>),
        ] : Array<Dynamic>);
        final my_data = ([
            "a" => ([
                "b" => ([
                    "c" => deep,
                ] : Map<String, Dynamic>),
            ] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
