$(function () {

    flag1 = false;  //表示用户名输入是否合法
    flag2 = false;  //表示密码输入是否合法
    flag3 = false;  //表示确认密码输入是否合法
    flag4 = false;  //表示邮箱输入是否合法

    // 用户名
    $('#username').change(function () {
        var v = $(this).val();
        if (/^[a-zA-Z_]\w{5,17}$/.test(v)){

            flag1 = true;
            //如果输入格式正确，则验证用户名是否存在
            $.get('/app/checkusername/', {username: $(this).val()}, function (data) {
                // console.log(data)
                if (data.status == 1) {
                    $('#msg').html('用户名可以使用').css('color', 'green');
                }
                else if (data["status"] == 0) {
                    $('#msg').html(data.msg).css('color', 'red');
                }
                else if (data["status"] == -1) {
                    $('#msg').html('请求方式不正确').css('color', 'red');
                }
            })
        }
        else {

            flag1 = false;
            $('#msg').html('用户名输入有误').css('color', 'red');
        }
    });

    // 密码
    $('#password').change(function () {
        var v = $(this).val();
        if (/^.{8,}$/.test(v)){

            flag2 = true
            $('#msg_passwd').html('密码可以使用').css('color', 'green');
        }
        else {

            flag2 = false
            $('#msg_passwd').html('密码不合法').css('color', 'red');
        }
    });

    // 确认密码
    $('#again').change(function () {
        if ($(this).val() == $('#password').val()){
            flag3 = true
            $('#msg_passwd_check').html('可以使用').css('color', 'green');
        }
        else {

            flag3 = false
            $('#msg_passwd_check').html('两次输入不一致').css('color', 'red');
        }
    });

    // 邮箱
    $('#email').change(function () {
        var v = $(this).val();
        if (/^\w+@\w+\.\w+$/.test(v)){
            flag4 = true
            $('#msg_mail').html('邮箱可以使用').css('color', 'green');
        }
        else {
            flag4 = false
             $('#msg_mail').html('邮箱不合法').css('color', 'red');
        }
    });


    // 注册
    $('#register').click(function () {

        if (flag1 && flag2 && flag3 && flag4){
            return true
        }
        else {
            window.alert('请重新输入')
            return false
        }
    })




});
