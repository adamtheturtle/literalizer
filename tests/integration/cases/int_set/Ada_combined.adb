procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := ASet'(
            AInt (1),
            AInt (2),
            AInt (3)
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := ASet'(
            AInt (1),
            AInt (2),
            AInt (3)
        );
    end Check_Assignment;
begin
    null;
end Check;
