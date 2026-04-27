procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AMap'(1 .. 0 => ANull),
            AMap'(1 .. 0 => ANull)
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AMap'(1 .. 0 => ANull),
            AMap'(1 .. 0 => ANull)
        );
    end Check_Assignment;
begin
    null;
end Check;
