class Fixture_call_dotted_method_Haxe_call {
    public static function main() {
        var app = { client: { fetch: function(payload:Dynamic):Dynamic return null } };
        app.client.fetch("hello");
        app.client.fetch(42);
        app.client.fetch(true);
    }
}
