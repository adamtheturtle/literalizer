class Fixture_yaml_rebound_anchor_nested_Haxe {
    public static function main() {
        final my_data = ([
            "a" => ([1, ([2] : Array<Dynamic>), 2] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
