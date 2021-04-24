$(document).ready(function(){
    var accunt = document.getElementById("accunt")
    var accunterr = document.getElementById("accunterr")
    var checkerr = document.getElementById("checkerr")

    var pass = document.getElementById("pass")
    var passerr = document.getElementById("passerr")
    var passwd = document.getElementById("passwd")
    var passwderr = document.getElementById("passwderr")

    //当他聚焦,其他的两个都要消失
    accunt.addEventListener("focus", function(){
        accunterr.style.display = "none"
        checkerr.style.display = "none"
    },false)
    //当离焦的时候,要做一些验证了
    accunt.addEventListener("blur", function(){
        instr = this.value
        if (instr.length < 6 || instr.length > 12){
            accunterr.style.display = "block"
            return
        }
        //这个要和数据库判断的就必须得发起ajax请求了,这里专门写了一个视图验证账号是否已经被注册
        $.post("/checkuserid/", {"userid":instr}, function(data){
            if (data.status == "error"){
                checkerr.style.display = "block"
            }
        })
    },false)

    //聚焦的时候消失
    pass.addEventListener("focus", function(){
        passerr.style.display = "none"
    },false)
    //当离焦的时候,要做一些验证了
    pass.addEventListener("blur", function(){
        instr = this.value
        if (instr.length < 6 || instr.length > 16){
            passerr.style.display = "block"
            return
        }
    },false)

    //聚焦的时候消失
    passwd.addEventListener("focus", function(){
        passwderr.style.display = "none"
    },false)
    //当离焦的时候,要做一些验证了
    passwd.addEventListener("blur", function(){
        instr = this.value
        if (instr != pass.value){
            passwderr.style.display = "block"
            return
        }
    },false)

$(document).ready(function(){
    var sub = document.getElementById("zhuce")
    sub.addEventListener("click", function(){
        layer.open({
            type: 2
            ,content: '注册成功！登陆中,请耐心等待...'
          });
    });
})

$("#file").on('change', function () {
    console.log("我进来了啊！");
    var rd = new FileReader();//创建文件读取对象
    files = this.files[0];//获取file组件中的文件
    console.log(files)

    //判断图片类型,如果不需要判断去掉第一个if()就好
    let fileType = files.type.slice(6, 10)
    if (fileType != 'jpg' && fileType != 'png' && fileType != 'jpeg' && fileType != 'bmp') {
    alert('仅支持jpg、jpeg、gif、png、bmp格式的图片，请重新上传图片')
    return
    } else {
    rd.readAsDataURL(files);//文件读取装换为base64类型
    rd.onloadend = function (e) {
    //加载完毕之后获取结果赋值给img
    document.getElementById("img").src = this.result;
            }
        }
    })


})