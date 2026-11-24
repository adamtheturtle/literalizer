class Fixture_call_empty_container_type_hint_Haxe_call {
    public static function main() {
        function process(values:Dynamic, count:Dynamic):Dynamic return null;
        process(([1, ([] : Map<String, Dynamic>)] : Array<Dynamic>), 42);
    }
}
