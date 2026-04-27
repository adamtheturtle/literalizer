procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("lint", AList'(AInt (2), AList'(1 .. 0 => ANull))),
            AEntry ("test", AList'(AInt (5), AList'(AStr ("compile"))))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("lint", AList'(AInt (2), AList'(1 .. 0 => ANull))),
            AEntry ("test", AList'(AInt (5), AList'(AStr ("compile"))))
        );
    end Check_Assignment;
begin
    null;
end Check;
