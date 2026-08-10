Imports System.Collections.Generic
Module Check
    Sub _declaration()
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
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"a", New Dictionary(Of String, Object) From {
                ' inner note
                {"b", 1}  ' inline b
            }},
            {"list", New Integer() {
                1,  ' first
                2  ' second
            }}
        }
    End Sub
End Module
