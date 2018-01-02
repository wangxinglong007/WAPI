# !/usr/bin/python
# coding=utf-8


class TemplateHtml:

    def __init__(self):
        pass

    @staticmethod
    def get_report_html():
        report_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        {% load staticfiles %}
        <meta charset="UTF-8">
        <title>report</title>
        <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/4.0.0-beta/css/bootstrap.min.css">
        <script src="https://cdn.bootcss.com/jquery/3.2.1/jquery.min.js"></script>
        <script src="https://cdn.bootcss.com/popper.js/1.12.5/umd/popper.min.js"></script>
        <script src="https://cdn.bootcss.com/bootstrap/4.0.0-beta/js/bootstrap.min.js"></script>
        
        <link rel="stylesheet" href="{% static 'WEB_API/css/common/jquery-ui-1.10.4.custom.min.css' %}" />
        <script type="text/javascript"  src="{% static 'WEB_API/js/common/jquery-1.10.2.js' %}"></script>
        <script type="text/javascript"  src="{% static 'WEB_API/js/common/jquery-ui-1.10.4.custom.js' %}"></script>
        <script type="text/javascript"  src="{% static 'WEB_API/js/common/jquery-ui-1.10.4.custom.min.js' %}"></script>
        
        <link rel="stylesheet" href="E:\\ctrip\\work\\backup\\ApiCaseVersion\\ApiCaseSystem\\static\\WEB_API\\css\\common\\jquery-ui-1.10.4.custom.min.css" />
        <script type="text/javascript"  src="E:\\ctrip\\work\\backup\\ApiCaseVersion\\ApiCaseSystem\\static\\WEB_API\\js\\common\\jquery-1.10.2.js"></script>
        <script type="text/javascript"  src="E:\\ctrip\\work\\backup\\ApiCaseVersion\\ApiCaseSystem\\static\\WEB_API\\js\\common\\jquery-ui-1.10.4.custom.js"></script>
        <script type="text/javascript"  src="E:\\ctrip\\work\\backup\\ApiCaseVersion\\ApiCaseSystem\\static\\WEB_API\\js\\common\\jquery-ui-1.10.4.custom.min.js"></script>

        <script type="text/javascript">

            $(function(){
                $(".div_title").click(function(){
                    $(this).next().slideToggle();
                });
            });
        </script>
        <script type="text/javascript">
            $(function() {
            var title_content=$('.title_content');
            var i=0;
            for( var i = 0; i < title_content.length; i++ ) {
                    //alert(title_content.eq(i).children("td:last-child").html());
                    var result_td=title_content.eq(i).children("td:last-child");
                    if(result_td.html()!='Success'){
                        result_td.css('color','red');
                        result_td.parent().parent().parent().css('color','red');
                    }
            }
            });
        </script>
        
<style type="text/css">
    *{margin: 0;padding: 0}
    /*左侧API描述内容以及结果统计样式*/
    #left_bar{width: 17%;margin-left: 1%; margin-top: 1.5%;float: left; position:fixed;top:1%;left:1%;}
    #result_count{ margin-top: 4%;}
    #report_des ul :first-child,#result_count ul :first-child{font-size: 16px}
    #report_des ul,#result_count ul{ font-size: 14px; }
    /*右侧报告内容样式*/
    #right_bar{float: left;width:78%; margin-left: 2%; margin-top: 1%;-webkit-box-shadow: 0 0 5px #cccccc; padding: 0.5%;position: absolute;top: 1%; left: 19%}
    #report_div{}
    #report_th{background:#0084F3;color: white; height: 50px;}
    /*固定表格具体宽度*/
    /*
    #report_th table tr td{background: red;}
    .div_title table tr td{background: black;}*/
    #report_th table{width: 99%; height:100%;text-align: center;margin-left: 1%;border-collapse: separate;text-align:left;}
    /*用例ID*/
    #report_th .CaseID2{width: 5%;}
    /*接口名称*/
    #report_th .ApiName2{width: 18%;}
    /*用例中文描述*/
    #report_th .Description2{width: 24%;}
    /*编辑者*/
    #report_th .Editor2{width: 10%;}
    /*方法*/
    #report_th .Method2{width: 5%;}
    /*开始执行时间*/
    #report_th .ExecutionTime2{width: 12%;}
    /*执行消耗时间*/
    #report_th .UseTime2{width: 10%;}
    /**/
    #report_th .Expect2{width: 10%;}


    #report_div div:nth-child(even){display: none; padding-left:2%;padding-right:2%;background: #e7e7e7;word-wrap:break-word}
    .div_title{margin-left: 1%;}
    .div_title table{width: 99%;height:38px;text-align: center;border-collapse: separate;font-size: 12px;border-collapse: separate;table-layout: fixed;word-break: break-all; word-wrap: break-word;text-align: left;border-bottom:1px #DDD solid; }
    .div_title table tr td{overflow: hidden;text-overflow:ellipsis;white-space: nowrap;}
    .div_title .CaseID {width: 5%;}
    .div_title .ApiName {width: 18%;}
    .div_title .Description {width: 24.5%;}
    .div_title .Editor {width: 10%;}
    .div_title .Method {width: 5%;}
    .div_title .ExecutionTime {width: 12.5%;}
    .div_title .UseTime {width: 10%;}
    .div_title .Expect {width: 10%;}
    .div_title .Status {color: #6c6;font-weight:bold;}
    /*预期值相关*/
    .ExpectResult_div{}
    .ExpectResult{}
    .ExpectResult_content{display: none;width:80px;text-align:center; z-index: 2;word-wrap:break-word;margin-top: 10px;}
    xmp{font-size: 14px;font-family: 'Time New Romans'}
    {% ifequal api_type 1  %}
        #report_th {padding-left: 5.5%}
        .div_title {padding-left: 5%}
    {% endifequal %}

</style>
        </head>
        <body>
            <div id="mainview">
                <div id="left_bar">
                    <div id="report_des">
                        <ul class="list-group">
                        <li class="list-group-item active">API Automation Description</li>
                        <li class="list-group-item"><b>User:&nbsp;</b>{{ user }}</li>
                        <li class="list-group-item"><b>StartTime:&nbsp;</b>{{ start_time }}</li>
                        <li class="list-group-item"><b>UseTime:&nbsp;</b>{{ use_time }}</li>
                        <li class="list-group-item"><b>Success:&nbsp;</b>与预期值校验正确</li>
                        <li class="list-group-item"><b>Fail:&nbsp;</b>与预期值校验错误</li>
                        <li class="list-group-item"><b>Error:&nbsp;</b>用例格式数据/输入错误/返回结果有问题等 </li>
                        </ul>
                    </div>
            
                    <div id="result_count">
                        <ul class="list-group">
                        <li class="list-group-item active">Result Count</li>
            
                        <li class="list-group-item"><b>Total:&nbsp;</b>{{ counts.0 }}</li>
                        <li class="list-group-item"><b>Success:&nbsp;</b>{{ counts.1 }}</li>
                        <li class="list-group-item"><b>Fail:&nbsp;</b>{{ counts.2 }}</li>
                        <li class="list-group-item"><b>Error:&nbsp;</b>{{ counts.3 }}</li>
                    </div>
                </div>
                <div id="right_bar">
                        <div id="report_th">
                                <table >
                                    <tr>
                                        
                                        <td class="CaseID2">用例ID</td>
                                        {% ifequal api_type 0  %}
                                        <td class="ApiName2">接口名称</td>
                                        {% endifequal %}
                                        <td class="Description2">用例中文描述</td>
                                        <td class="Editor2">编辑者</td>
                                        <td class="Method2">方法</td>
                                        <td class="ExecutionTime2">开始执行时间</td>
                                        <td class="UseTime2">执行消耗时间</td>
                                        <td class="Expect2">预期值</td>
                                        <td class="Status2">结果</td>
                                        
                                        
                                        
                                    </tr>
                                </table>
                         </div>
                    <div id="report_div">
                        {% for result in result_list %}
                        <div class="div_title">
                            <table>
                                <tr class="title_content">
                                <td class="CaseID">{{ result.CaseID }}</td>
                                {% ifequal api_type 0  %}
                                <td class="ApiName" title="{{ result.ApiName }}">{{ result.ApiName }}</td>
                                {% endifequal %}
                                <td class="Description" title="{{ result.Description }}">{{ result.Description }}</td>
                                <td class="Editor">{{ result.Editor }}</td>
                                <td class="Method">{{ result.Method }}</td>
                                <td class="ExecutionTime">{{ result.ExecutionTime }}</td>
                                <td class="UseTime">{{ result.UseTime }}</td>
                                <td class="Expect" title="{{ result.Expect }}">
                                {{ result.Expect }}
                                </td>
                                <td class="Status">{{ result.Status }}</td>
                                </tr>
                            </table>
                        </div>
                        {% ifequal api_type 1  %}
                            <div>
                                <pre style="height=auto;">{{ result.APIResult }}</pre>
                            </div>
                        {% else %}
                            <div>
                                {{ result.APIResult }}
                            </div>
                        {% endifequal %}
                        {% endfor %}
                    </div>
                </div>
            </div>
        </body>
        </html>"""
        return report_html
