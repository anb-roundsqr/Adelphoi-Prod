from django.template import loader
from .models import ModelTests
from django.http import JsonResponse, FileResponse
import os
import weasyprint
from datetime import datetime
from weasyprint import CSS
from rest_framework.response import Response
import logging
from AdelphoiProject.settings import BASE_DIR,STATICFILES_DIRS
logging.basicConfig(
    filename='test_log.log',
    level=logging.INFO,
    filemode='a',
    format='%(asctime)s'
           ' %(process)d-%(name)-12s'
           ' %(levelname)-8s -%(funcName)s  -  %(lineno)d'
           '     %(message)s')

# Get an instance of a logger
logger = logging.getLogger(__name__)


def index(request, *args, **kwargs):
    template = loader.get_template('index2.html'
    )  # getting our template
    try:
        results = ModelTests.objects.filter(client_code=kwargs['pk'])[0]
        logger.info('Pdf generation based on client_code %s', results)
    except:
        logger.info('ClientCode is not exists for PDF generation')
        return JsonResponse({"result": "ClientCode not exist"})
    if results.Exclusionary_Criteria == True:
        exc_crt = "Rejected"
    else:
        exc_crt = "Accepted"
    if len(results.client_selected_program) <= 0:
        recommnded_program = None
    else:
        recommnded_program = results.client_selected_program
    if results.confidence == None:
        confidence_var = None
    else:
        confidence_var = str(results.confidence) + "%"
    if results.roc_confidence == None:
        roc_confidence_var = None
    else:
        roc_confidence_var = str(results.roc_confidence) + "%"
    values = {
        'name': results.name,
        'last_name':results.last_name,
        'refer_status': exc_crt,
        'confidence': confidence_var,
        'roc_confidence': roc_confidence_var,
        'recommended_program': recommnded_program,
        'recommende_level': results.client_selected_program
    }
    dirs = os.path.join(BASE_DIR,"Adelphoi_outputfiles")
    date_path = str(datetime.now().strftime('%Y-%m-%d'))
    try:
        logger.info('directory is creating for pdf')
        os.makedirs(dirs + '/' + 'outputfiles/' + date_path + '/' +
                    str(results.client_code) + '/')
	#print("location creared")
    except:
        pass
    reportfilename = str(str(results.client_code) + ".pdf")
    pdf_file_path = dirs + '/' + 'outputfiles/' + date_path + '/'
    pdf_file_path += str(results.client_code) + '/' + reportfilename
    print("path",pdf_file_path)
    html = template.render(
        values
    )  # Renders the template with the context data.
    pdf = weasyprint.HTML(
        string=html,
        base_url=request.build_absolute_uri()
    ).write_pdf(
        stylesheets=[
            CSS(os.path.join(STATICFILES_DIRS[0],"css","index.css"))
        ],
        presentational_hints=True
    )
    open(pdf_file_path, 'wb').write(pdf)
    try:
        logger.info('Pdf file response')
        return FileResponse(open(pdf_file_path, 'rb'),
                            content_type='application/pdf')
    except:
        logger.info('error in generating PDF page')
        return Response({"Response": "file not found"})
