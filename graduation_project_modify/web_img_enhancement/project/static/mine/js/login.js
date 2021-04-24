$(document).ready(function(){
    var sub = document.getElementById("denglu")
    sub.addEventListener("click", function(){
        layer.open({
            type: 2
            ,content: '登陆中,请耐心等待'
          });
    });

    var error1 = $("#error").html().trim();
    if( error1 == '密码错误')
    {
        console.log(error1);
        layer.open({
               content: 'oh！密码错误，请重新输入'
               ,skin: 'msg'
               ,time: 2 //2秒后自动关闭
        });
    }else if (error1 == "该用户不存在")
    {
        console.log(error1);
        layer.open({
               content: '您输入的用户不存在'
               ,skin: 'msg'
               ,time: 2 //2秒后自动关闭
        });
    }
})