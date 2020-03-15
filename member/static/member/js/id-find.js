$('#findid').submit(function() {
    var email = $('#email').val()
    $.ajax({
        url:'member/id-find',
        data: {'email':email},
        success:function(data) {
            $('#user-id').html(data)
        },
        error:function(e) {
            $('#user-id').html(e)
        }
    })
})