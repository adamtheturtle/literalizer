Imports System.Collections.Generic
Module Check
    Dim Deep = New String()() {
        New String() {
            "one",
            "two"
        },
        New String() {
            "three",
            "four"
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
