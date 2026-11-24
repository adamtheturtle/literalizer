class Fixture_call_empty_mapping_receiver_parameter_Haxe_call {
    public static function main() {
        var api = { process: function(self:Dynamic):Dynamic return null };
        api.process(([] : Map<String, Dynamic>));
    }
}
