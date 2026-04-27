procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AStr ("48656c6c6f")
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AStr ("48656c6c6f")
        );
    end Check_Assignment;
begin
    null;
end Check;
