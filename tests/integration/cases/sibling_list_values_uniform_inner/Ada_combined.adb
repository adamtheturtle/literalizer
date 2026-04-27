procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("lint", AList'(AInt (2), AList'(AInt (1)))),
            AEntry ("test", AList'(AInt (5), AList'(AInt (7))))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("lint", AList'(AInt (2), AList'(AInt (1)))),
            AEntry ("test", AList'(AInt (5), AList'(AInt (7))))
        );
    end Check_Assignment;
begin
    null;
end Check;
