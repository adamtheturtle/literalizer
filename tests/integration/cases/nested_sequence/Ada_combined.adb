procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            ABool (True),
            AStr ("hi"),
            AList'(AInt (1), AInt (2)),
            ANull
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            ABool (True),
            AStr ("hi"),
            AList'(AInt (1), AInt (2)),
            ANull
        );
    end Check_Assignment;
begin
    null;
end Check;
