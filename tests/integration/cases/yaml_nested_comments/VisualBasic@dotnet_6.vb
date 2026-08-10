Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", New Dictionary(Of String, Object) From {
            ' inner note
            {"b", 1}  ' inline b
        }},
        {"list", New Integer() {
            1,  ' first
            2  ' second
        }}
    }
End Module
