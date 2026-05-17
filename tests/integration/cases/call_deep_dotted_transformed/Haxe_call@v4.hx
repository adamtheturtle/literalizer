class Fixture_call_deep_dotted_transformed_Haxe_call {
    public static function main() {
        var app = { client: { fetch: function(payload:Dynamic):Dynamic return null } };
        function emit(_arg:Dynamic):Dynamic return null;
        emit(app.client.fetch("hello"));
        emit(app.client.fetch(42));
        emit(app.client.fetch(true));
    }
}
