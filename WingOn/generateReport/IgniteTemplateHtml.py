# !/usr/bin/python
# coding=utf-8


class IgniteTemplateHtml:

    def __init__(self):
        pass

    @staticmethod
    def get_report_html():
        report_html = """
        <html lang="en"><head>
        <meta charset="UTF-8">
        <title>点火结果报告</title>
        <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/4.0.0-beta/css/bootstrap.min.css">
        <script src="https://cdn.bootcss.com/jquery/3.2.1/jquery.min.js"></script>
        <script src="https://cdn.bootcss.com/popper.js/1.12.5/umd/popper.min.js"></script>
        <script src="https://cdn.bootcss.com/bootstrap/4.0.0-beta/js/bootstrap.min.js"></script>
        
        <link rel="stylesheet" href="/static/css/jquery-ui-1.10.4.custom.min.css">
        <script src="/static/js/jquery-1.10.2.js"></script>
        <script src="/static/js/jquery-ui-1.10.4.custom.js"></script>
        <script src="/static/js/jquery-ui-1.10.4.custom.min.js"></script>
        <script type="text/javascript">

        </script>
        <script type="text/javascript">
            $(function() {
            var status=$('.status');
            var i=0;
            for(var i=0;i<status.length;i++){
                if(status.eq(i).html()!='200'){
                    status.eq(i).parent().css({'color':'red','background':'#EEEEEE'});
                }
            }

            });
        
        </script>
        
        
        
        
        <style type="text/css">
            *{margin: 0;padding: 0}
            /*左侧API描述内容以及结果统计样式*/
            #left_bar{width: 17%;margin-left: 1%; margin-top: 1.5%;float: left;	position:fixed;top:1%;left:1%;}
            #result_count{ margin-top: 4%;}
            #report_des ul :first-child,#result_count ul :first-child{font-size: 16px}
            #report_des ul,#result_count ul{ font-size: 14px; }
            /*右侧报告内容样式*/
            #right_bar{float: left;width:78%; margin-left: 2%; margin-top: 1%;-webkit-box-shadow: 0 0 5px #cccccc; padding: 0.5%;position: absolute;top: 1%; left: 19%}
            #report_div{}
            #report_th{font-size: 12px;text-align: center;}
            #report_th table{}
            #report_th table tr th{background: #0084F3;color: white;text-align: left;font-size: 14px;}
        
            /*固定表格具体宽度*/
            /*
            #
            .div_title table tr td{background: black;}*/
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
                        <li class="list-group-item"><b>Success:&nbsp;</b>与预期结果校验正确（ExpectResult）</li>
                        <li class="list-group-item"><b>Fail:&nbsp;</b>与预期结果校验错误（ExpectResult） </li>
                        <li class="list-group-item"><b>Error:&nbsp;</b>用例格式数据或输入错误 </li>
                        </ul>
                    </div>
        
                    <div id="result_count">
                        <ul class="list-group">
                        <li class="list-group-item active">Result Count</li>
                        <li class="list-group-item"><b>Total:&nbsp;</b>{{ counts.0 }}</li>
                        <li class="list-group-item"><b>Status_200:&nbsp;</b>{{ counts.1 }}</li>
                        <li class="list-group-item"><b>Status_Other:&nbsp;</b>{{ counts.2 }}</li>
                    </ul></div>
                </div>
                <div id="right_bar">
                        <div id="report_th" class="table-responsive">
                                <table id="table_result" class="table">
                        <tbody><tr>
                            <th>ID</th>
                            <th>SystemType</th>
                            <th>ApiName</th>
                            <th>Method</th>
                            <th>Status</th>
                            <th>ExecutionTime</th>
                            <th>UseTime (S)</th>
                        </tr>
                        <tr>
                        {% for result in result_list %}
                            <td>{{ result.0 }}</td>
                            <td>{{ result.1 }}</td>
                            <td title='{{ result.2 }}'>{{ result.2 }}</td>
                            <td>{{ result.3 }}</td>
                            <td class="status">{{ result.4 }}</td>
                            <td>{{ result.5 }}</td>
                            <td>{{ result.6 }}</td>
                        </tr>
                        {% endfor %}
                
                                </tbody></table>
                         </div>
                </div>
            </div>
        
        </body></html>"""
        return report_html
