procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AFloat (3.14);
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AFloat (3.14);
    end Check_Assignment;
begin
    null;
end Check;
