class Fixture_call_cpp_identity_bound_method_Haxe_call {
    public static function main() {
        var thing = { go: function(value:Dynamic):Dynamic return null };
        final item = ([
            1,
            2,
        ] : Array<Dynamic>);
        thing.go(item);
    }
}
