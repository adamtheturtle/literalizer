procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            -- # section
            AStr ("a")
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            -- # section
            AStr ("a")
        );
    end Check_Assignment;
begin
    null;
end Check;
