with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AMap'[
        -- comment
        AEntry ("name", AStr ("Alice")),
        AEntry ("score", ANull)
    ];
begin
    my_data := AMap'[
        -- comment
        AEntry ("name", AStr ("Alice")),
        AEntry ("score", ANull)
    ];
end Check;
