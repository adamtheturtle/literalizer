procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("name", AStr ("Alice")),
            AEntry ("age", AInt (30)),
            AEntry ("active", ABool (True)),
            AEntry ("score", ANull),
            AEntry ("joined", AStr ("2024-01-15")),
            AEntry ("last_login", AStr ("2024-01-15T12:30:00+00:00")),
            AEntry ("avatar", AStr ("48656c6c6f"))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("name", AStr ("Alice")),
            AEntry ("age", AInt (30)),
            AEntry ("active", ABool (True)),
            AEntry ("score", ANull),
            AEntry ("joined", AStr ("2024-01-15")),
            AEntry ("last_login", AStr ("2024-01-15T12:30:00+00:00")),
            AEntry ("avatar", AStr ("48656c6c6f"))
        );
    end Check_Assignment;
begin
    null;
end Check;
