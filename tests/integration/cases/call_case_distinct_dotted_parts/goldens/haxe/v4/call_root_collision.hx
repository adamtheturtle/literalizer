class Fixture_call_case_distinct_dotted_parts_Haxe_call_root_collision {
    public static function main() {
        var foo = { Foo: { bar: function(x:Dynamic):Dynamic return null } };
        foo.Foo.bar(([1] : Array<Dynamic>));
    }
}
