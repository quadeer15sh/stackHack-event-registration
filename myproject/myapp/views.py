from django.shortcuts import render, HttpResponse, redirect
from django.core import serializers
import cv2
import numpy as np
from django.contrib.staticfiles.storage import staticfiles_storage
from face_detection.face import detect_image, cropped_image, readb64
from myapp.models import Members, Event
from PIL import Image
import pytesseract
from fuzzywuzzy import fuzz
import re
import json
import uuid
import base64
from django.core.files.base import ContentFile

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Create your views here.


def index(request):
    events = Event.objects.all()

    if 'submit' in request.POST:

        img = cv2.imdecode(np.fromstring(
            request.FILES['file'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
        request.session['name'] = request.POST.get('name')
        request.session['event'] = request.POST.get('event')
        request.session['email'] = request.POST.get('email')
        request.session['phone'] = int(request.POST.get('phone'))
        request.session['type'] = request.POST.get('type')
        request.session['tickets'] = int(request.POST.get('tickets'))
        # could be png, update html as well
        ret, frame_buff = cv2.imencode('.jpg', img)
        image_id = base64.b64encode(frame_buff)
        request.session['image_id'] = f"data:image/jpg;base64,{image_id.decode('utf-8')}"

        n = detect_image(img)
        string = pytesseract.image_to_string(Image.open(request.FILES['file']))

        if n == 0:
            status = 1
            return render(request, 'myapp/index.html', {'status': status,'events':events})

        score = 0
        if string:
            s = string.split('\n')
            for word in s:
                score = fuzz.token_set_ratio(request.POST.get('name'), s)
                if score > 86:
                    break

        if score < 86:
            status = 2
            return render(request, 'myapp/index.html', {'status': status,'events':events})


        return redirect('preview')

    try:
        page = request.session['redirect']
    except:
        page = None

    if page:
        request.session['redirect'] = False
        context = {
            'name': request.session['name'],
            'phone': request.session['phone'],
            'email': request.session['email'],
            'events':events
        }

        return render(request, 'myapp/index.html', context)
    return render(request, 'myapp/index.html',{'events':events})


def preview(request):

    status = True

    keys = ['name', 'email', 'phone', 'type', 'tickets', 'image_id']

    try:
        context = {
            'status': status,
            'name': request.session['name'],
            'email': request.session['email'],
            'phone': request.session['phone'],
            'type': request.session['type'],
            'tickets': request.session['tickets'],
            'image_id': request.session['image_id'],
            'event':request.session['event']
        }
    except KeyError:
        return redirect('index')

    if 'edit' in request.POST:
        status = False
        request.session['redirect'] = True
        return redirect('index')

    if 'submit' in request.POST:
        image = request.session['image_id']
        img = readb64(request.session['image_id'])
        frame = cropped_image(img)
        string_code = f"data:image/jpg;base64,{frame.decode('utf-8')}"
        res = uuid.uuid1().hex.upper()[:-22]

        formats, imgstr = image.split(';base64,') 
        ext = formats.split('/')[-1] 

        data = ContentFile(base64.b64decode(imgstr), name=f'{res}.' + ext)
        e = Event.objects.get(name=request.session['event'])

        try:
            member = Members.objects.get(email=request.session['email'])
            context['status'] = 3
            return render(request, 'myapp/preview.html', context)
        except Members.DoesNotExist:
            member = Members(name=request.session['name'],email=request.session['email'],
                            phone=request.session['phone'],reg_type=request.session['type'],
                            tickets=request.session['tickets'],photo_id=data,reg_number=res,event=e)
            member.save()

        member_obj = serializers.serialize('json',[member],ensure_ascii=False)[1:-1]
        d = json.loads(member_obj) 

        request.session['member'] = d['fields']
        request.session['code'] = string_code

        return redirect('event')

    return render(request, 'myapp/preview.html', context)


def event(request):

    e = Event.objects.get(name=request.session['event'])

    context = {
        'member':request.session['member'],
        'code': request.session['code'],
        'event':e
    }

    keys = ['name', 'email', 'phone', 'type', 'tickets', 'image_id']

    try:
        for key in keys:
            del request.session[key]
    except KeyError:
        return redirect('index')

    return render(request, "myapp/show.html", context)

