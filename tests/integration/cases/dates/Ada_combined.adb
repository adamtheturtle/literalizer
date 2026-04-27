with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AMap'[
        AEntry ("date", AStr ("2024-01-15")),
        AEntry ("datetime", AStr ("2024-01-15T12:30:00+00:00"))
    ];
begin
    my_data := AMap'[
        AEntry ("date", AStr ("2024-01-15")),
        AEntry ("datetime", AStr ("2024-01-15T12:30:00+00:00"))
    ];
end Check;
