with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        -- null heading
        -- before null
        AEntry ("a", ANull),  -- first null
        AEntry ("b", ANull)  -- second null
    ];
begin
    null;
end Main;
