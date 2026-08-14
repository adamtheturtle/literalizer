with A_Stub; use A_Stub;
procedure Main is
    deep : A_Val := AList'[
        AList'[
            AStr ("one"),
            AStr ("two")
        ],
        AList'[
            AStr ("three"),
            AStr ("four")
        ]
    ];
    my_data : A_Val := AMap'[
        AEntry ("a", AMap'[
            AEntry ("b", AMap'[
                AEntry ("c", deep)
            ])
        ])
    ];
begin
    null;
end Main;
