$(function () {

    //+
    $('.add').click(function () {
        // console.log("add: " + this);
        // var num = $(this).prev();
        var that = this;

        //先获取要修改数量的购物车id： cartid
        var cartid = $(this).parents('.menuList').attr('cartid');

        //ajax
        $.get('/app/addnum/', {'cartid': cartid}, function(data) {
            // console.log(data)
            //如果修改成功，则将页面中对应的数量节点改变
            if (data.status == 1){
                $(that).prev().html(data.num)
            }
            else {
                console.log(data.msg)
            }

            //重新计算总价
            calculate();
        })

    });

    // -
    $('.reduce').click(function () {
        var cartid = $(this).parents('.menuList').attr('cartid');
        var that = this;

        $.get('/app/reducenum/', {'cartid': cartid}, function(data) {
            // console.log(data)
            if (data.status == 1){
                $(that).next().html(data.num)
            }
            else {
                console.log(data.msg)
            }

            //重新计算总价
            calculate();
        })
    });

    //删除
    $('.delbtn').click(function () {
        var cartid = $(this).parent().attr('cartid');
        var that = this;

        //ajax
        $.get('/app/deletecart/', {'cartid': cartid}, function(data) {
            // console.log(data)
            // location.reload()  //刷新页面
            if (data.status == 1){
                $(that).parent().remove();  //删除节点
            }
            else {
                console.log(data.msg)
            }

            // 重新判断是否全选
            isAllSelected()
        })

    });


    //勾选/取消勾选
    $('.select').click(function () {
        var cartid = $(this).parents('.menuList').attr('cartid');
        var that = this;

        //ajax
        $.get('/app/cartselect/', {cartid: cartid}, function(data) {
            // console.log(data)
            if (data.status == 1) {
                // if (data.is_select1) {
                //     $(that).find('span').html('√');
                // }
                // else {
                //     $(that).find('span').html('');
                // }
                $(that).find('span').html( data.is_select1 ? '√' : '' );
            }
            else {
                console.log(data.msg)
            }

            // 重新判断是否全选
            isAllSelected()

        });

    });


    //全选
    $('#allselect').click(function () {
        //1,如果当前全部勾选了，则全不选,将所有的都不勾选
        //2,如果有未勾选的，则全选，将未勾选的勾选

        //先判断是否全部勾选了
        selects = [];  // 保存所有选中cartid
        unselects = [];  // 保存所有未选中的cartid

        //遍历所有的li
        // for (var i=0; i<$('.menuList').length; i++){
        //     $('.menuList').eq(i)
        // }
        $('.menuList').each(function() {
            var select = $(this).find('.select').children('span').html();
            if (select){
                //如果是勾选的，则添加到selects中
                selects.push($(this).attr('cartid'))
            }
            else {
                //如果未勾选，则添加到unselects中
                unselects.push($(this).attr('cartid'))
            }
        });

        // 如果当前全部都勾选了，则执行全不选
        if (unselects.length == 0){
            //ajax
            $.get('/app/cartselectall/', {'action': 'cancelselect', 'selects': selects.join('#')}, function(data) {
                // console.log(data)
                if (data.status == 1){
                    $('.select').find('span').html('')
                }
                else {
                    console.log(data.msg)
                }

                // 重新判断是否全选
                isAllSelected()
            });
        }
        // 如果当前未全部勾选，则执行全选
        else {
            //ajax
            $.get('/app/cartselectall/', {'action': 'select', 'selects': unselects.join('#')}, function(data) {
                // console.log(data)
                if (data.status == 1){
                    $('.select').find('span').html('√')
                }
                else {
                    console.log(data.msg)
                }

                // 重新判断是否全选
                isAllSelected()
            });
        }



    });


    // 检测是否全选了
    isAllSelected();
    function isAllSelected(){
        var count = 0;
        $('.select').each(function () {
            if ($(this).find('span').html()){
                count++;
            }
        });

        //如果全选了
        if (count == $('.select').length){
            $('#allselect').find('span').html('√')
        }
        //否则不打勾
        else {
            $('#allselect').find('span').html('')
        }

        //重新计算总价
        calculate();

    }


    // 计算总价
    function calculate() {

        //总价
        total = 0;

        //遍历所有的li
        $('.menuList').each(function() {
            if ($(this).find('.select').find('span').html()){
                //如果是勾选的，则计算价格
                price = parseFloat($(this).find('.price').html()); //单价
                num = parseInt($(this).find('.num').html());  //数量
                total += price * num;

            }
        });

        // 显示总价
        $('#totalprice').html(total.toFixed(2));
    }


});





