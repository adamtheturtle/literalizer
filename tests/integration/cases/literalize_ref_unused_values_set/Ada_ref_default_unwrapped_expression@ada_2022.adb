with A_Stub; use A_Stub;
procedure Main is
    procedure Consume_Widget (Arg_Value : A_Val) is begin null; end Consume_Widget;
begin
    Consume_Widget(arg_value => ASet'[
        AInt (1),
        AInt (2)
    ]);
end Main;
