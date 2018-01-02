$(function(){
    $('#sub_case_id').attr("disabled","disabled");
    $('#soap_system_code').css('display','none');
});
//主用例/子用例切换响应事件
function chg(){
    if(document.getElementById("sel").value=="0"){

        $('#sub_case_id').attr("disabled","disabled");
        $('#sub_case_id').val('');
    }
    else{
    	$('#sub_case_id').removeAttr("disabled");
    	$('#sub_case_id').val('');

    }
};

//SoapAPI/RestAPI切换响应事件
function changeType(){
    if(document.getElementById("api_type").value=="SoapAPI"){
        document.getElementById("soap_system_code").style.display='';
        document.getElementById("system_code").style.display='none';
    }else{
        document.getElementById("soap_system_code").style.display='none';
        document.getElementById("system_code").style.display='';
    }
}
    $(function() {
    $( "#click_time" ).datetimepicker({
         format:'Y-m-d H:i:s',
         step:10
    });
    $( "#end_time" ).datetimepicker({
         format:'Y-m-d H:i:s',
         step:10
    });
    });


//日志详情展开 方法
function logSlideToggle(){
    $(".div_title").click(function(){
        $(this).next().slideToggle();
    });
}
//状态颜色 方法
function statusColor(){
    var table_content=$('.table_content');
    var i=0;
    for( var i = 0; i < table_content.length; i++ ) {

            var result_td=table_content.eq(i).children("td:last-child");
            if(result_td.html()=='Fail'){
                result_td.css('color','#c60');
            }
            else if(result_td.html()=='Error'){
                result_td.css('color','#c00');
            }
            else if(result_td.html()=='Success'){
                result_td.css('color','#6c6');
            }else{
                ;
            }
    }
}
//分页链接 点击响应 方法
function linkClick(){
    $('a').click(function(){
        var oLink=$(this).attr('href');
        //alert(oLink);
        $.ajax({
         url: oLink,
         success: function(result, statues, xml){
            //alert('进入分页回调');
            //alert(result);
            $("#response_result").html(result);
            logSlideToggle();
            statusColor();
            linkClick();
         },
         error: function(){
            alert("false");
         },
         dataType: "html"
        });
        return false;
    });
}
//页面加载完成 方法  查询提交请求
$(document).ready(function(){
    $.ajaxSetup({
        data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
    });
    //查询提交 get请求
    $('#submit_btn').click(function(){
        //alert('进入submit');
        var csrfmiddlewaretoken='{{ csrf_token }}';
        var api_type = $("#api_type").val();
        var case_type = $("#sel").val();
        var click_time = $("#click_time").val();
        var end_time = $("#end_time").val();
        var system_code = $("#system_code").val();
        var soap_system_code = $("#soap_system_code").val();
        var environment = $("#environment").val();
        var case_id = $("#case_id").val();
        var sub_case_id = $("#sub_case_id").val();
        //正整数正则表达式 1-9开头
        var reg=/^[1-9]\d*$|^0$/;
        if(click_time==''||end_time==''){
            alert('开始时间和结束时间不能为空');
            $("#click_time").focus();
            return false;
        }else if(click_time>end_time){
            alert('开始时间不能早于结束时间');
            $("#click_time").focus();
            return false;
        }else if(case_type=='1'&&(case_id&&!(sub_case_id)||(sub_case_id&&(!case_id)))){
                if(case_id&&!(sub_case_id)){alert('有主用例ID时 必须输入子用例ID');$("#sub_case_id").focus();}
                else{alert('有子用例ID时 必须输入主用例ID');$("#case_id").focus();}
                return false;
        }else if(case_type=='1'&&!(!case_id&&!sub_case_id)&&(reg.test(case_id)==false||reg.test(sub_case_id)==false)){
            alert('请输入正确的ID');
            return false;
        }else if(case_type=='0'&&case_id&&reg.test(case_id)==false){
            alert('请输入正确的主用例ID');
            $("#case_id").focus();
            return false;
        }
        else{
            document.getElementById("loading").style.display='block';
            document.getElementById("loading").style.opacity='0.6';
            $.ajax({
                type:"GET",
                data: {api_type:api_type,case_type:case_type,click_time:click_time,
                        end_time:end_time,system_code:system_code,soap_system_code:soap_system_code,
                        environment:environment,case_id:case_id,sub_case_id:sub_case_id},
                url: "/log/",
                cache: false,
                dataType: "html",
                /*ajax成功时回调方法*/
                success: function(result, statues, xml){
                    //关闭 loading
                    document.getElementById("loading").style.display='none';
                    //局部刷新数据
                    $("#response_result").html(result);
                    //加载分页提交事件
                    linkClick();
                    //加载数据下拉事件
                    logSlideToggle();
                    //加载状态颜色事件
                    statusColor();
                },
                error: function(){
                    alert("false");
                }
            });
            return false;
        }
    });
});
