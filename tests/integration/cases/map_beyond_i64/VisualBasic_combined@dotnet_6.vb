Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"a", 9223372036854775807UL},
            {"b", 9223372036854775808UL}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"a", 9223372036854775807UL},
            {"b", 9223372036854775808UL}
        }
    End Sub
End Module
