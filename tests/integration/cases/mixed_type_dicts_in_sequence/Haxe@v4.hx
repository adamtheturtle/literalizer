class Fixture_mixed_type_dicts_in_sequence_Haxe {
    public static function main() {
        final my_data = ([
            (["type" => "create", "pr_id" => "pr_1", "draft" => true] : Map<String, Dynamic>),
            (["type" => "create", "pr_id" => "pr_2"] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
