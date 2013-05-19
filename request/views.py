from django.http import HttpResponse
from django.template import RequestContext, loader
import qr


def ticket(request):
    params = request.GET.get('params', '')
    qrEncoder = qr.QRencode()
    data = params.split(',')
    info, qrHash = qrEncoder.getData(int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4]))
    qrImage = qrEncoder.generate(qrHash)
    shortHash = qrHash[0:7]
    qrEncoder.saveToDB(str(qrImage), str(info), str(qrHash), str(shortHash))
    qrStorage = '/site_media/static/img/'
    f = qrStorage + qrImage + '.png'
    ticket = f

    t = loader.get_template('ticket.html')
    c = RequestContext(request, {'ticket': ticket, 'hash': shortHash})
    return HttpResponse(t.render(c))


def check(request):
    params = request.GET.get('ticket', '')
    qrEncoder = qr.QRencode()
    checkHash = qrEncoder.verifyHash(params)
    shortHash = params[0:7]
    if checkHash == 'VALID':
        response = 'Valid ticket'
        error_flag = 0
    elif checkHash == 'INVALID':
        response = 'Not valid ticket'
        shortHash = 'No hash provided'
        error_flag = 0
    else:
        response = 'Unexpected error!!!'
        error_flag = 1

    t = loader.get_template('verify.html')
    c = RequestContext(request, {'response': response, 'flag': error_flag, 'ticketId': shortHash})
    return HttpResponse(t.render(c))