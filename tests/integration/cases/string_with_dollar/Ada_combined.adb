procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AStr ("price $10"),
            AStr ("$HOME")
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AStr ("price $10"),
            AStr ("$HOME")
        );
    end Check_Assignment;
begin
    null;
end Check;
