with A_Stub; use A_Stub;
procedure Main is
    deep : A_Val := AList'[
        AList'[
            AInt (1),
            AInt (2)
        ],
        AList'[
            AInt (3),
            AInt (4)
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
