with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("item", AStr ("existing"))],
        -- This comment describes the next item.
        AMap'[AEntry ("item", AStr ("next"))]
    ];
begin
    my_data := AList'[
        AMap'[AEntry ("item", AStr ("existing"))],
        -- This comment describes the next item.
        AMap'[AEntry ("item", AStr ("next"))]
    ];
end Main;
