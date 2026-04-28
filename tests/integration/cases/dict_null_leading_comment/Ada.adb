with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        -- comment
        AEntry ("name", AStr ("Alice")),
        AEntry ("score", ANull)
    ];
begin
    null;
end Main;
