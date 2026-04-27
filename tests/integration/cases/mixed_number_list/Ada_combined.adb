procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AInt (1),
            AFloat (2.5),
            AInt (3)
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AInt (1),
            AFloat (2.5),
            AInt (3)
        );
    end Check_Assignment;
begin
    null;
end Check;
