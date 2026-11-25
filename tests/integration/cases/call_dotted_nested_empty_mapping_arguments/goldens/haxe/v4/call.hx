class Fixture_call_dotted_nested_empty_mapping_arguments_Haxe_call {
    public static function main() {
        var api = { worker: { process: function(values:Dynamic, count:Dynamic):Dynamic return null } };
        api.worker.process(([1, ([] : Map<String, Dynamic>)] : Array<Dynamic>), 42);
        api.worker.process(([2, (["x" => "s"] : Map<String, Dynamic>)] : Array<Dynamic>), 43);
    }
}
