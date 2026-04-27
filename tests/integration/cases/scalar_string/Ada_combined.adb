procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AStr ("hello");
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AStr ("hello");
    end Check_Assignment;
begin
    null;
end Check;
