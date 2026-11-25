with A_Stub; use A_Stub;
procedure Main is
    procedure Consume_Widget (Arg_Value : A_Val) is begin null; end Consume_Widget;
    a : A_Val := AInt (0);
    my_data : A_Val := AList'[
        a,
        AInt (1)
    ];
begin
    Consume_Widget(arg_value => my_data);
end Main;
