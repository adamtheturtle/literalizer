with A_Stub; use A_Stub;
procedure Main is
    procedure Consume_Widget (Arg_Value : A_Val) is begin null; end Consume_Widget;
    item : A_Val := ANull;
    my_data : A_Val := ANull;
    Consume_Widget(arg_value => my_data);
begin
    my_data := item;
    Consume_Widget(arg_value => my_data);
end Main;
