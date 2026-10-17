class Fixture_yaml_rebound_anchor_multiple_Haxe {
    public static function main() {
        final my_data = ([
            "a" => ([1, ([2, 3] : Array<Dynamic>), 3] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
