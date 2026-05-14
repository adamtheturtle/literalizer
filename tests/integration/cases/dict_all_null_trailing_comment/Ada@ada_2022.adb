with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", ANull),
        AEntry ("b", ANull)
        -- trailing
    ];
begin
    null;
end Main;
