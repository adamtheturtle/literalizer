Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", New Object() {
            1L
        }},
        {"b", New Object() {
            1099511627776L
        }}
    }
End Module
