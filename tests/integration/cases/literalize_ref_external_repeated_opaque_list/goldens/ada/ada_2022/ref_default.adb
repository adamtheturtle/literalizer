with A_Stub; use A_Stub;
procedure Main is
    procedure Consume_Widget (Arg_Value : A_Val) is begin null; end Consume_Widget;
    item : A_Val := AList'[];
    my_data : A_Val := AList'[
        item,
        item
    ];
begin
    Consume_Widget(arg_value => my_data);
end Main;
