Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Long() {
            1L,
            1099511627776L
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Long() {
            1L,
            1099511627776L
        }
    End Sub
End Module
