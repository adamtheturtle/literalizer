with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AMap'[
        AEntry ("message", AStr ("no comment here"))
    ];
begin
    my_data := AMap'[
        AEntry ("message", AStr ("no comment here"))
    ];
end Check;
