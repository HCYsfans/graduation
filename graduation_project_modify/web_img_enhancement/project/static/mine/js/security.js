$(document).ready(function(){

$(document).ready(function(){
    var sub = document.getElementById("xiugai")
    sub.addEventListener("click", function(){
        layer.open({
            type: 2
            ,content: '修改成功！稍后请重新登录...'
          });
    });
})
    var useraccount = document.getElementById("useraccount").innerHTML;
    console.log(useraccount)

    var oldpass = document.getElementById("oldpass")
    var newpass1 = document.getElementById("newpass1")
    var newpass2 = document.getElementById("newpass2")

    var olderr = document.getElementById("olderr")
    var pass1err =document.getElementById("pass1err")
    var pass2err =document.getElementById("pass2err")

    //聚焦的时候消失
    oldpass.addEventListener("focus", function(){
        olderr.style.display = "none"
    },false)
    //当离焦的时候,要做一些验证了
    oldpass.addEventListener("blur", function(){
        old_psd = this.value
        $.post("/checkuserpsd/", {"useraccount":useraccount,"userpsd":old_psd}, function(data){
            if (data.status == "error"){
                olderr.style.display = "block"
            }
        })
    },false)

    //聚焦的时候消失
    newpass1.addEventListener("focus", function(){
        pass1err.style.display = "none"
    },false)
    //当离焦的时候,要做一些验证了
    newpass1.addEventListener("blur", function(){
        instr = this.value
        if (instr.length < 6 || instr.length > 16){
            pass1err.style.display = "block"
            return
        }
    },false)

    //聚焦的时候消失
    newpass2.addEventListener("focus", function(){
        pass2err.style.display = "none"
    },false)
    //当离焦的时候,要做一些验证了
    newpass2.addEventListener("blur", function(){
        pass1 = newpass1.value
        pass2 = newpass2.value
        if (pass1 != pass2){
            pass2err.style.display = "block"
            return
        }
    },false)

})