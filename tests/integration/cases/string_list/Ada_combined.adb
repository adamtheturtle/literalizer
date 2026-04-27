procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AStr ("foo"),
            AStr ("bar"),
            AStr ("baz")
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AStr ("foo"),
            AStr ("bar"),
            AStr ("baz")
        );
    end Check_Assignment;
begin
    null;
end Check;
