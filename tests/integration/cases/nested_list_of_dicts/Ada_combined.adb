procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AList'(AMap'(AEntry ("name", AStr ("Alice"))), AMap'(AEntry ("name", AStr ("Bob")))),
            AList'(AMap'(AEntry ("name", AStr ("Charlie"))), AMap'(AEntry ("name", AStr ("Dave"))))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AList'(AMap'(AEntry ("name", AStr ("Alice"))), AMap'(AEntry ("name", AStr ("Bob")))),
            AList'(AMap'(AEntry ("name", AStr ("Charlie"))), AMap'(AEntry ("name", AStr ("Dave"))))
        );
    end Check_Assignment;
begin
    null;
end Check;
