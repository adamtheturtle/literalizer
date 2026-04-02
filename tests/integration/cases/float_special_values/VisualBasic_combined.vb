Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Double() {
            inf,
            -inf,
            nan
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Double() {
            inf,
            -inf,
            nan
        }
    End Sub
End Module
