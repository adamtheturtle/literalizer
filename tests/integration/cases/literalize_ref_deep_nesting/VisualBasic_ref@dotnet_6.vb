Imports System.Collections.Generic
Module Check
    Dim Deep = New Integer()() {
        New Integer() {
            1,
            2
        },
        New Integer() {
            3,
            4
        }
    }
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", New Dictionary(Of String, Object) From {
            {"b", New Dictionary(Of String, Object) From {
                {"c", Deep}
            }}
        }}
    }
End Module
