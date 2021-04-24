$(document).ready(function(){

    var wdlw = $("#wdlw").html();
    console.log(wdlw)
    if (wdlw == "您还未登录,请先登录")
    {
        console.log(wdlw);
        layer.open({
            content: '您还未登录,请先登录'
            ,btn: '好的'
        });
    }


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

$("#file2").on('change', function () {
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
    document.getElementById("img2").src = this.result;
            }
        }
    })

  var success1 = document.getElementById("success1")
  var success2 = document.getElementById("success2")
  var antutip = document.getElementById("antutip")
  var trans_1 = document.getElementById("trans_p1")
  var trans_2 = document.getElementById("trans_p2")
  var trans_3 = document.getElementById("trans_f1")
  var sp1 = document.getElementById("a1")
  var sp2 = document.getElementById("a2")
  var sp3 = document.getElementById("a3")
  var sp4 = document.getElementById("a4")
  var sp5 = document.getElementById("a5")
  var sp6 = document.getElementById("a6")
  var sp7 = document.getElementById("a7")
  var sp8 = document.getElementById("a8")
  var sp9 = document.getElementById("a9")
  var sp10 = document.getElementById("a10")
  var picname= document.getElementById("pic_name")
  var tippp = document.getElementById("tippp")

  //当他聚焦,错误提示要消失
    picname.addEventListener("focus", function(){
        tippp.style.display = "none"
    },false)

  //当离焦的时候,要做一些验证了
    picname.addEventListener("blur", function(){
        instr = this.value
        //这个要和数据库判断的就必须得发起ajax请求了,这里专门写了一个视图验证账号是否已经被注册
        $.post("/check/2/", {"name":instr}, function(data){
            if (data.status == "error"){
                tippp.style.display = "block"
            }
        })
    },false)

  //var quwutip = document.getElementById("quwutip")
  if (window.location.pathname=='/handle/1/')
  {
    antutip.style.display="block";
    sp1.style.display="block";
  }
  else if(window.location.pathname=='/handle/2/')
  {
    sp2.style.display="block";
  }
  else if(window.location.pathname=='/handle/3/')
  {
    trans_1.style.display="block";
    trans_2.style.display="block";
    trans_3.style.display="block";
    trans_3.required=true;
    sp3.style.display="block";
  }
  else if(window.location.pathname=='/handle/4/')
  {
    sp4.style.display="block";
  }
  else if(window.location.pathname=='/handle/5/')
  {
    sp5.style.display="block";
  }
  else if(window.location.pathname=='/handle/6/')
  {
    sp6.style.display="block";
  }
  else if(window.location.pathname=='/handle/7/')
  {
    sp7.style.display="block";
  }
  else if(window.location.pathname=='/handle/8/')
  {
    sp8.style.display="block";
  }
  else if(window.location.pathname=='/handle/9/')
  {
    sp9.style.display="block";
  }
  else if(window.location.pathname=='/handle/10/')
  {
    sp10.style.display="block";
  }

var sub = document.getElementById("sub")
sub.addEventListener("click", function(){
    layer.open({
        type: 2
        ,content: '处理中,请稍后'
      });
});

try{
  var baocun = document.getElementById("bc")
  var shanchu = document.getElementById("sc")
  var result_display = document.getElementById("result_display")
  baocun.addEventListener("click", function(){
        console.log("bc")
        var pathname = window.location.pathname;
        console.log(pathname)
        layer.open({
        content: '您确定要保存吗？'
        ,btn: ['保存', '取消']
        ,yes: function(index){
            $.post("/check/0/",{"suggest":"123"},function(data){
              if (data.status == "success" )
              {
                    layer.open({
                        content: '恭喜您！保存成功~'
                        ,skin: 'msg'
                        ,time: 2 //2秒后自动关闭
                  });
              }
            })
        }
      },false)
      setTimeout(function(){window.location.href = "http://127.0.0.1:8001"+pathname;},3000);

});

  shanchu.addEventListener("click", function(){
        console.log("sc")
        var pathname = window.location.pathname;
        console.log(pathname)
        layer.open({
        content: '您确定要删除吗？'
        ,btn: ['删除', '取消']
        ,yes: function(index){
                $.post("/check/1/",{"suggest":"123"},function(data){
                if (data.status == "success" )
                {
                    layer.open({
                        content: '恭喜您！删除成功~'
                        ,skin: 'msg'
                        ,time: 2 //2秒后自动关闭
                    });
                }
            })
            layer.close(index);
            }
        })
     setTimeout(function(){window.location.href = "http://127.0.0.1:8001"+pathname;},3000);
  },false)
}catch(exception){
    console.log("未操作页面")
}

})


