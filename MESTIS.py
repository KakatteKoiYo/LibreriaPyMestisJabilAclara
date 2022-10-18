#####################################################################
#                                                                   #
# Libreria de Python para obtener datos de MESTIS para Aclara RF    #
# Daniel_Romo@jabil.com                                             #
#                                                                   #
#####################################################################
from xml.etree import ElementTree
import requests

### getMasterFaster() regresa un string con el serial Master ligado al serial 2D ingresado como parametro 
### Método más rápido que getMasterFrom2D para traer el serial master, pero no recomendado en unidades con un largo historial como las golden
def getMasterFaster(serial2D:str, host:str = "mxgdlm0webte02") -> str:
    try:
        url = "http://" + host + "/wsMesInterface/MesWebServiceInterface.asmx/GetBoardHistoryFromMesInstance"

        parametros = {"mesInstance" : "1", "customerID" : "68", "serialNumber" : serial2D }
        respuesta = requests.get(url, params = parametros)
        respuestaTexto = respuesta.text

        respuestaXML = respuestaTexto.replace("&lt;", "<").replace("&gt;", ">")
        
        parsedXML = ElementTree.fromstring(respuestaXML)
        serialrespuesta = parsedXML[0][1].text

        return serialrespuesta
    except:
        return "Serial Linked Not Founded"

### getMasterFrom2D() regresa un string con el serial Master ligado al serial 2D ingresado como parametro 
def getMasterFrom2D(serial2D:str, host:str = "mxgdlm0webte02") -> str:
    try:
        url = "http://" + host + "/OkToTesterWebServiceInterface/OkToTesterWebServiceInterface.asmx/GetMesSerialFromLinkedCode"

        parametros = {"customer" : "ACLARA", "linkedCode" : serial2D, "instance" : "1"}
        respuesta = requests.get(url, params = parametros)
        respuestaTexto = respuesta.text

        respuestaXML = respuestaTexto.replace("&lt;", "<").replace("&gt;", ">")
        
        parsedXML = ElementTree.fromstring(respuestaXML)
        serialrespuesta = parsedXML.text
        
        return serialrespuesta
    except:
        return "Serial Linked Not Founded"

### getAclaraWhiteList() regresa un string del whitelist de Aclara (en este vienen por ejemplo todos los seriales Golden registrados así como fixtures y demás)
def getAclaraWhiteList(host:str = "mxgdlm0webte02") -> str :
    try:
        url = "http://" + host + "/OkToTesterWebServiceInterface/OkToTesterWebServiceInterface.asmx/GetWhiteListFromCustomer"

        parametros = {"customer" : "ACLARA"}
        respuestaWhiteList = requests.get(url, params = parametros)
        respuestaWhiteListTexto = respuestaWhiteList.text

        respuestaWhiteListXML = respuestaWhiteListTexto.replace("&lt;", "<").replace("&gt;", ">")
        
        parsedXML = ElementTree.fromstring(respuestaWhiteListXML)
        aclaraWhiteList = parsedXML.text
        
        return aclaraWhiteList
    except:
        return "An error ocurred"

### getCurrentlyHoldStatus() regresa un valor booleano (True o False) dependiendo del estado OnHold del serial ingresado como parametro
def getCurrentlyHoldStatus(serial:str, host:str = "mxgdlm0webte02") -> bool|str:
    try:
        url = "http://" + host + "/wsMesInterface/MesWebServiceInterface.asmx/LookupCustAssyFromMesInstance"

        parametros = {"mesInstance" : "1", "serialNumber" : serial, "customerName" : "ACLARA", "division" : "ACLARA RF"}
        respuestaHold = requests.get(url, params = parametros)
        respuestaHoldTexto = respuestaHold.text

        respuestaHoldXML = respuestaHoldTexto.replace("&lt;", "<").replace("&gt;", ">")
        
        parsedXML = ElementTree.fromstring(respuestaHoldXML)
        isHoldstr = parsedXML[0][0][12].text
        if isHoldstr.strip() == "true":
            isHold = True
        else:
            isHold = False
        return isHold
    except:
        return "An error ocurred"

### getCurrentStep() regresa dos valores del último paso y status del serial ingresado como parametro
### Ejemplo de uso : (paso, estatus) = getCurrentStep(serial), de esta forma se "desempacan" los valores step y status
def getCurrentStep(serial:str, host:str = "mxgdlm0webte02") -> tuple|str:
    try:
        url = "http://" + host + "/wsMesInterface/MesWebServiceInterface.asmx/GetCurrentRouteStepFromMesInstance"

        parametros = {"mesInstance" : "1", "serialNumber" : serial}
        respuestaStep = requests.get(url, params = parametros)
        respuestaStepTexto = respuestaStep.text

        respuestaStepXML = respuestaStepTexto.replace("&lt;", "<").replace("&gt;", ">")
        
        parsedXML = ElementTree.fromstring(respuestaStepXML)
        step = parsedXML[0][0][6].text
        status = parsedXML[0][0][14].text
        
        return step, status
    except:
        return "An error ocurred"

### getRevision() regresa un string con la revisión del serial ingresado como parametro
def getRevision(serial:str, host:str = "mxgdlm0webte02") -> str:
    try:
        url = "http://" + host + "/wsMesInterface/MesWebServiceInterface.asmx/GetBoardHistoryFromMesInstance"

        parametros = {"mesInstance" : "1", "customerID" : "68", "serialNumber" : serial }
        respuesta = requests.get(url, params = parametros)
        respuestaTexto = respuesta.text

        respuestaXML = respuestaTexto.replace("&lt;", "<").replace("&gt;", ">")
        
        parsedXML = ElementTree.fromstring(respuestaXML)
        revision = parsedXML[0][3].text

        return revision
    except:
        return "An error ocurred"