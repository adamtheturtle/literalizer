class Fixture_literalize_ref_pre_indented_injected_text_Haxe_ref {
    public static function main() {
                    final shared = ([
                        1,
                        2,
                    ] : Array<Dynamic>);
                    final other = 3;
                    final payload = "\n    shared : Val\nshared = RInt 99";
                    final my_data = ([
                        "a" => shared,
                        "b" => other,
                        "payload" => payload,
                    ] : Map<String, Dynamic>);
    }
}
