procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AList'(AInt (1), AInt (2)),
            AList'(1 .. 0 => ANull),
            AList'(AStr ("a"), AStr ("b"))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AList'(AInt (1), AInt (2)),
            AList'(1 .. 0 => ANull),
            AList'(AStr ("a"), AStr ("b"))
        );
    end Check_Assignment;
begin
    null;
end Check;
