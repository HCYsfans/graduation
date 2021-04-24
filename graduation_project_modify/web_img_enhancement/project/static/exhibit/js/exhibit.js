$(document).ready(function(){

  var showtypebtn = document.getElementById("showtypebtn")
  var selectdelete = document.getElementById("selectdelete")

  var typediv = document.getElementById("typediv")

    typediv.style.display = "none"
    console.log("############################")

    showtypebtn.addEventListener("click", function(){
        typediv.style.display = "block"
    },false)

    typediv.addEventListener("click", function(){
        typediv.style.display = "none"
    },false)

  var modifys = document.getElementsByClassName("xiugai");
  var deletes = document.getElementsByClassName("shanchu");

  //给所有的删除添加点击事件
    for(var i = 0; i<deletes.length;i++)
    {
        del = deletes[i];
        del.addEventListener("click",function(){
            bianhao = this.getAttribute("bianhao")
            layer.open({
                content: '您确定要删除该图片吗？'
                ,btn: ['确定', '取消']
                ,yes: function(index){
                   //操作
                   $.post("/manipulate/0/",{"bianhao":bianhao},function(data){

                      if (data.status == "success" )
                      {
                          layer.open({
                                content: '恭喜您！删除成功~'
                                ,skin: 'msg'
                                ,time: 2 //2秒后自动关闭
                          });
                      }else{
                        //失败了
                      }
                   })

                }
            });
        setTimeout(function(){location.reload();},2300);
        });
    }

    //给所有的修改添加点击事件
    for(var i = 0; i<modifys.length;i++)
    {
        modify = modifys[i];
        modify.addEventListener("click",function(){
            bianhao = this.getAttribute("bianhao")
            console.log(bianhao)
            layer.open({
                id:1,
                type: 1,
                title:'修改名称',
                skin:'layui-layer-rim',
                area:['8rem', 'auto'],
                content: ' <div class="row" style="width: 8rem;  margin-left:7px; margin-top:10px;">'
                    +'<div class="col-sm-12">'
                    +'<div class="input-group">'
                    +'<span class="input-group-addon"> 新 名 称   :</span>'
                    +'<input id="newname" class="newname" placeholder="请输入名称">'
                    +'</div>'
                    +'</div>'
                    +'</div>'
                ,btn:['保存','取消']
                ,yes: function(index){
                    var newname = document.getElementById("newname");
                    name= newname.value
                    console.log(name)
                    $.post("/manipulate/1/",{"bianhao":bianhao,"newname":name},function(data){

                      if (data.status == "success" )
                      {
                            layer.open({
                                content: '恭喜您！修改成功~'
                                ,skin: 'msg'
                                ,time: 2 //2秒后自动关闭
                            });
                            layer.close(index)
                            setTimeout(function(){location.reload();},2300);
                      }else{
                            layer.open({
                                content: '不好意思，已有该名称！，请重新命名'
                                ,skin: 'msg'
                                ,time: 2 //2秒后自动关闭
                            });
                      }
                   })

                }
    });

        });
    }

    var wdlw = $("#wdlw").html();
    if (wdlw == "您还未登录,请先登录")
    {
        console.log(wdlw);
          layer.open({
            content: '您还未登录,请先登录'
            ,skin: 'msg'
            ,time: 3 //3秒后自动关闭
          });
    }

//    var else1 = document.getElementById("else1")
//    var color = document.getElementById("color")
//
//    if (window.location.pathname=='/exhibit/3/')
//    {
//        console.log("ex3")
//        color.style.display="block";
//        else1.style.display="none";
//    }
//    else{
//        console.log("else");
//        color.style.display="none";
//        else1.style.display="block";
//    }

});