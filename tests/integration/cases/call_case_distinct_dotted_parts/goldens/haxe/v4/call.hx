class Fixture_call_case_distinct_dotted_parts_Haxe_call {
    public static function main() {
        var a = { foo: { Foo: { bar: function(x:Dynamic):Dynamic return null } } };
        a.foo.Foo.bar(([1] : Array<Dynamic>));
    }
}
