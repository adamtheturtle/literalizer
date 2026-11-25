class Fixture_record_two_shapes_Haxe {
    public static function main() {
        final my_data = ([
            "metrics" => (["count" => 100, "rate" => 50] : Map<String, Dynamic>),
            "flags" => (["retries" => 3, "timeout" => 30] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
