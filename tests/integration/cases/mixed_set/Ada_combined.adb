procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := ASet'(
            ABool (True),
            AInt (42),
            AStr ("apple")
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := ASet'(
            ABool (True),
            AInt (42),
            AStr ("apple")
        );
    end Check_Assignment;
begin
    null;
end Check;
