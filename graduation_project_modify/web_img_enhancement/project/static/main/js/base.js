window.onload = function(){
    $(document).ready(function(){
        document.documentElement.style.fontSize = innerWidth / 10 + "px";
    })
    var pathname = window.location.pathname;
    if(pathname=='/home/')
    {
        $( '#home1' ).css({
            'background' : 'url(/static/main/img/home1.png) no-repeat' ,
            'background-size' : '0.513889rem'
        });
        $( '#home2' ).css({
            'color': '#7BC1D7'
        });
    }else if(pathname.search("/handle/") != -1){
        //console.log("aaaaa")
        $( '#handle1' ).css({
            'background' : 'url(/static/main/img/handle1.png) no-repeat' ,
            'background-size' : '0.513889rem'
        });
        $( '#handle2' ).css({
            'color': '#7BC1D7'
        });
    }else if(pathname.search("/exhibit/") != -1){

        $( '#exhibit1' ).css({
            'background' : 'url(/static/main/img/exhibit1.png) no-repeat' ,
            'background-size' : '0.513889rem'
        });
        $( '#exhibit2' ).css({
            'color': '#7BC1D7'
        });
    }else if(pathname=='/mine/'){

        $( '#mine1' ).css({
            'background' : 'url(/static/main/img/mine1.png) no-repeat' ,
            'background-size' : '0.513889rem'
        });
        $( '#mine2' ).css({
            'color': '#7BC1D7'
        });
    }

}