class Fixture_call_cpp_identity_nested_method_Haxe_call {
    public static function main() {
        var outer = { thing: { go: function():Dynamic return null } };
        outer.thing.go();
    }
}
