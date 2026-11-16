with A_Stub; use A_Stub;
procedure Main is
    procedure Consume_Widget (Arg_Value : A_Val) is begin null; end Consume_Widget;
    my_data : A_Val := AInt (0);
    shared : A_Val := AInt (1);
begin
    my_data := shared;
    Consume_Widget(arg_value => my_data);
end Main;
