Imports System.Collections.Generic
Module Check
    Function consume_widget(arg_value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim ref_data = New Integer() {
            1,
            2
        }
        Dim my_data = New Integer() {
            0
        }
        consume_widget(my_data)
        my_data = ref_data
        consume_widget(my_data)
    End Sub
End Module
