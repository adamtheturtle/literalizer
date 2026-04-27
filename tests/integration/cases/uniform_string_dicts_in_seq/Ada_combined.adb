procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AMap'(AEntry ("first", AStr ("Alice")), AEntry ("last", AStr ("Smith"))),
            AMap'(AEntry ("first", AStr ("Bob")), AEntry ("last", AStr ("Jones")))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AMap'(AEntry ("first", AStr ("Alice")), AEntry ("last", AStr ("Smith"))),
            AMap'(AEntry ("first", AStr ("Bob")), AEntry ("last", AStr ("Jones")))
        );
    end Check_Assignment;
begin
    null;
end Check;
