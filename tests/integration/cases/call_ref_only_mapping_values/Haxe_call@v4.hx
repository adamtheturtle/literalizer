class Fixture_call_ref_only_mapping_values_Haxe_call {
    public static function main() {
        function consume(value:Dynamic):Dynamic return null;
        final item = 42;
        consume((["field" => item] : Map<String, Dynamic>));
    }
}
