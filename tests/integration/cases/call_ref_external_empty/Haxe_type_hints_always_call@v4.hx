class Fixture_call_ref_external_empty_Haxe_type_hints_always_call {
    public static function main() {
        function consume(value:Dynamic):Dynamic return null;
        final item:Array<Dynamic> = ([
            1,
            2,
        ] : Array<Dynamic>);
        consume(item);
    }
}
