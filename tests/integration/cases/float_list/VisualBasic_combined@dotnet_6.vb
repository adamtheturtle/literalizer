Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Double() {
            1.1,
            -2.2,
            3.3
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Double() {
            1.1,
            -2.2,
            3.3
        }
    End Sub
End Module
