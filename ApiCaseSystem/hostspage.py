import time,platform,os
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt 

hostsfile = '/etc/hosts'


def basepage(request, issuccess=0):
    now = time.strftime('%Y-%m-%d %X', time.localtime())
    with open(hostsfile) as f:
        hostsconent = f.read()
    return render_to_response('hostconfig.html', {'text': hostsconent, 'info': issuccess, 'now': now})


@csrf_exempt
def hostupdate(request):
    if request.POST.has_key('save'):
        contents = request.POST['content'].encode('utf-8')
        with open(hostsfile,'w+') as f:
            f.write(contents.replace('\r', ''))
        issuccess = 1
    elif request.POST.has_key('saveandfresh'):
        contents = request.POST['content'].encode('utf-8')
        with open(hostsfile,'w+') as f:
            f.write(contents.replace('\r', ''))
        if platform.system() == 'Windows':
            os.system('ipconfig /flushdns')
        elif platform.system() == 'Linux':
            os.system('systemctl restart network')
        issuccess = 1
    else:
        issuccess = 0
    return basepage(request, issuccess)

