# Copyright 2016 Team DriverCity. All Rights Reserved.

# [START app]
import spark_logging
import config

from flasgger import Swagger, swag_from, validate, ValidationError
from flask import Flask,request,abort,request

import payment
from cloud_storage_io import CloudStorageIO
from parking_event_repo import ParkingEventRepository
from occupancy_rates_repo import OccupancyRatesRepository
from utils import CronUtils

app = Flask(__name__)
Swagger(app)
app.config.from_object(config)
logger = spark_logging.get_logger(app.config['LOGGER_NAME'])


@app.route('/api/v1.0/parkingEvent/', methods=['POST'])
@swag_from('swagger_specs/parkingEvent.yml')
def store_parking_event():
    try:
        # validate schema
        validate(request.json, 'ParkingEvent', 'swagger_specs/parkingEvent.yml', root=__file__)

        # validate payment if paid context
        if request.json['parkingContextType'] == 'PAID':
            if not payment.is_test_payment(request.json,
                                           app.config['PAYMENT_VALIDATION_TEST_METHOD_TYPE'],
                                           app.config['PAYMENT_VALIDATION_TEST_RECEIPT']) :
                payment.validate(request.json)

        # store valid information
        store_result = ParkingEventRepository().store_parking_event(request.json, app.config['PARKING_EVENT_FIREBASE_TIME_IN_SECONDS'])
        return store_result, 201

    except ValidationError as e:
        logger.exception(e)
        abort(400)
    except payment.PaymentException as e:
        logger.exception(e)
        abort(400)
    except Exception as e:
        pass

    abort(500)


@app.route('/tasks/occupancy', methods=['GET'])
def update_occupancy_rates():
    """
    An API for updating the occupancy rates. Used by a cron schedule.
    ---
    tags:
      - Occupancy rates analysis task
    """
    try:
        CronUtils.require_cron(request.headers)
        counts = ParkingEventRepository().get_occuring_paid_event_counts()
        OccupancyRatesRepository().refresh_occupancies(counts)
        return '', 201
    except CronUtils.NotCronCallerException as e:
        logger.exception(e)
        abort(401)
    except Exception as e:
        logger.exception(e)

    abort(500)


@app.route('/tasks/store', methods=['GET'])
def move_to_long_term_data_store():
    """
    An API for storing the parking events to the long term data store. Used by a cron schedule.
    ---
    tags:
      - Blob storage task
    """
    try:
        CronUtils.require_cron(request.headers)
        new_events = ParkingEventRepository().consume_new_parking_events_by('willBeStoredToLongTermDataStore', True, False)
        CloudStorageIO(app.config['GOOGLE_CLOUD_STORAGE_STORE_NAME'],
                       app.config['GOOGLE_CLOUD_STORAGE_BLOB_NAME_PREFIX']).upload_to_parking_event_store(new_events)
        return '', 201
    except CronUtils.NotCronCallerException as e:
        logger.exception(e)
        abort(401)
    except Exception as e:
        logger.exception(e)

    abort(500)


@app.route('/tasks/cleanup', methods=['GET'])
def cleanup_firebase():
    """
    An API for removing dead parking events from firebase. Used by a cron schedule.
    ---
    tags:
      - Cleanup firebase task
    """
    try:
        CronUtils.require_cron(request.headers)
        ParkingEventRepository().remove_dead_events()
        return '', 201
    except CronUtils.NotCronCallerException as e:
        logger.exception(e)
        abort(401)
    except Exception as e:
        logger.exception(e)

    abort(500)


@app.errorhandler(500)
def server_error(e):
    logger.exception('An error occured', e)
    return """
    An internal error occurred.
    See logs for full stacktrace.
    """, 500

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
