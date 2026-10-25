with A_Stub; use A_Stub;
procedure Main is
    procedure Consume_Widget (Arg_Value : A_Val) is begin null; end Consume_Widget;
    item : A_Val := AList'[
        AInt (1),
        AInt (2)
    ];
    my_data : A_Val := AList'[
        AInt (1),
        AInt (2)
    ];
begin
    Consume_Widget(arg_value => my_data);
    my_data := item;
    Consume_Widget(arg_value => my_data);
end Main;
