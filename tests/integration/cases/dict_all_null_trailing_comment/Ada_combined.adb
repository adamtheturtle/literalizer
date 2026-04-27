with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AMap'[
        AEntry ("a", ANull),
        AEntry ("b", ANull)
        -- trailing
    ];
begin
    my_data := AMap'[
        AEntry ("a", ANull),
        AEntry ("b", ANull)
        -- trailing
    ];
end Check;
