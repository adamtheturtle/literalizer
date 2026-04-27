procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("users", AList'(AMap'(AEntry ("name", AStr ("Bob")), AEntry ("tags", AList'(AStr ("admin"), AStr ("user")))), AMap'(AEntry ("name", AStr ("Carol")), AEntry ("tags", AList'(AStr ("guest"))))))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("users", AList'(AMap'(AEntry ("name", AStr ("Bob")), AEntry ("tags", AList'(AStr ("admin"), AStr ("user")))), AMap'(AEntry ("name", AStr ("Carol")), AEntry ("tags", AList'(AStr ("guest"))))))
        );
    end Check_Assignment;
begin
    null;
end Check;
