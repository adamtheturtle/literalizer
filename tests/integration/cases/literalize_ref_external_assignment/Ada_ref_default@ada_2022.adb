with A_Stub; use A_Stub;
procedure Main is
    procedure Consume_Widget (Arg_Value : A_Val) is begin null; end Consume_Widget;
    ref_data : A_Val := AList'[
        AInt (1),
        AInt (2)
    ];
    my_data : A_Val := AList'[
        AInt (0)
    ];
    Consume_Widget(arg_value => my_data);
begin
    my_data := ref_data;
    Consume_Widget(arg_value => my_data);
end Main;
