$(document).ready(function(){

$(document).ready(function(){
    var sub = document.getElementById("xiugai")
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