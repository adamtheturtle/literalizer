with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[
            AMap'[AEntry ("item", AStr ("existing"))],
            AStr ("kept")
            -- This comment trails the first pair.
        ],
        AList'[AMap'[AEntry ("item", AStr ("next"))], AStr ("also kept")],
        -- This comment describes the last pair.
        AList'[AMap'[AEntry ("item", AStr ("last"))], AStr ("kept too")]
    ];
begin
    my_data := AList'[
        AList'[
            AMap'[AEntry ("item", AStr ("existing"))],
            AStr ("kept")
            -- This comment trails the first pair.
        ],
        AList'[AMap'[AEntry ("item", AStr ("next"))], AStr ("also kept")],
        -- This comment describes the last pair.
        AList'[AMap'[AEntry ("item", AStr ("last"))], AStr ("kept too")]
    ];
end Main;
