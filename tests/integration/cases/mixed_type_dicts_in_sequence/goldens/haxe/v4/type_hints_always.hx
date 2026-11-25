class Fixture_mixed_type_dicts_in_sequence_Haxe_type_hints_always {
    public static function main() {
        final my_data:Array<Dynamic> = ([
            (["type" => "create", "pr_id" => "pr_1", "draft" => true] : Map<String, Dynamic>),
            (["type" => "create", "pr_id" => "pr_2"] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
