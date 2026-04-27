procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AInt (0),
            AInt (1),
            AInt (-1)
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AInt (0),
            AInt (1),
            AInt (-1)
        );
    end Check_Assignment;
begin
    null;
end Check;
