import logging
import threading

from flask import Flask, request, abort, jsonify

from . import FridgeController, CtoF


logging.basicConfig(level=logging.DEBUG)

TEMP_ID = 'temp'
F_ID = 'F'
C_ID = 'C'

UPPER_LIMIT_ID = 'upper_limit'
LOWER_LIMIT_ID = 'lower_limit'
DELAY_ID = 'delay'
FRIDGE_ON_ID = 'fridge_on'

def check_for_temp(d):
    if TEMP_ID in d:
        return d[TEMP_ID]
    if F_ID in d:
        return d[F_ID]
    if C_ID in d:
        logging.debug(d[C_ID])
        return CtoF( float(d[C_ID]) )
    return None

fridgeController = FridgeController()

app = Flask(__name__)

@app.route('/')
def index():
    result = True
    if request.method == 'GET':
        if UPPER_LIMIT_ID in request.args:
            result = result and fridgeController.setUpperLimit(request.args[UPPER_LIMIT_ID])
        if LOWER_LIMIT_ID in request.args:
            result = result and fridgeController.setLowerLimit(request.args[LOWER_LIMIT_ID])
        if DELAY_ID in request.args:
            result = result and fridgeController.setDelay(request.args[DELAY_ID])

        if not result:
            abort(400)
        
        d = {
            UPPER_LIMIT_ID:fridgeController.upper_limit,
            LOWER_LIMIT_ID:fridgeController.lower_limit,
            FRIDGE_ON_ID:fridgeController.fridge_on,
            DELAY_ID:fridgeController.delay,
            TEMP_ID:fridgeController.tempF
        }

        return jsonify(d)

@app.route(f'/{UPPER_LIMIT_ID}', methods=['GET','POST'])
def upper_limit():
    if request.method == 'POST':
        temp = check_for_temp(request.form)
        if not temp:
            abort(400, "No temperature limit ('F', 'C') supplied")
        
    elif request.method == 'GET':
        temp = check_for_temp(request.args)
        if not temp:
            return str(fridgeController.upper_limit)

    if fridgeController.setUpperLimit(temp):
        return "Success"
    else:
        abort(400, f"Invalid temperature, {temp}")

@app.route(f'/{LOWER_LIMIT_ID}', methods=['GET','POST'])
def lower_limit():
    if request.method == 'POST':
        temp = check_for_temp(request.form)
        if not temp:
            abort(400, "No temperature limit ('F', 'C') supplied")
        
    elif request.method == 'GET':
        temp = check_for_temp(request.args)
        if not temp:
            return str(fridgeController.lower_limit)

    if fridgeController.setLowerLimit(temp):
        return "Success"
    else:
        abort(400, f"Invalid temperature, '{temp}'")

@app.route(f'/{FRIDGE_ON_ID}', methods=['GET'])
def getFridge_on():
    return str(fridgeController.fridge_on)

@app.route(f'/{DELAY_ID}',methods=['GET','POST'])
def delay():
    return str(fridgeController.delay)
        
@app.route(f'/{TEMP_ID}')
def temp():
    return str(fridgeController.tempF)

if __name__ == '__main__':

    ctrl = threading.Thread(target = fridgeController.run, name = "fridgeController")

    ctrl.start()
    logging.info("Controller Started")

    app.run(debug=True)

    logging.info("Exiting")

    fridgeController.quit = True
    ctrl.join()

    logging.info("Controller Stopped")
