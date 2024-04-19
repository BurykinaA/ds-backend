import logging
from flask import Flask, request, jsonify
from models.plate_reader import PlateReader, InvalidImage
import logging
import io
import requests
import functools
from image_provider_client import ImageProviderClient


app = Flask(__name__)
plate_reader = PlateReader.load_from_file("./model_weights/plate_reader_model.pth")
image_provider_client = ImageProviderClient("http://178.154.220.122:7777")


def error_handler(f):
    """
    A decorator to wrap the route in a try-except block
    to handle errors uniformly.
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except InvalidImage:
            logging.error("Invalid image")
            return jsonify({"error": "Invalid image"}), 400
        except Exception as e:
            logging.error(f"Error: {e}")
            return jsonify({"error": "Internal server error"}), 500

    return wrapper


@app.route("/")
def hello():
    user = request.args["user"]
    return f'<h1 style="color:red;"><center>Hello {user}!</center></h1>'


# <url>:8080/greeting?user=me
# <url>:8080 : body: {"user": "me"}
# -> {"result": "Hello me"}
@app.route("/greeting", methods=["POST"])
def greeting():
    if "user" not in request.json:
        return {"error": 'field "user" not found'}, 400

    user = request.json["user"]
    return {
        "result": f"Hello {user}",
    }


# <url>:8080/readPlateNumber : body <image bytes>
# {"plate_number": "c180mv ..."}
@app.route("/readPlateNumber", methods=["POST"])
def read_plate_number():
    im = request.get_data()
    im = io.BytesIO(im)

    try:
        res = plate_reader.read_text(im)
    except InvalidImage:
        logging.error("invalid image")
        return {"error": "invalid image"}, 400

    return {
        "plate_number": res,
    }


# <url>:8080/idToNum?pict_id='123'
# <url>:8080 : body: {"pict_id": "123"}
# -> {"plate_number": "с181мв190"}
@app.post("/idToNum")
@error_handler
def id_to_number():
    pict_id = request.json.get("pict_id", "")
    im_data = image_provider_client.get_image(pict_id)

    if im_data is None:
        return jsonify({"error": "Failed to fetch image"}), 404

    im = io.BytesIO(im_data)
    try:
        res = plate_reader.read_text(im)
        return jsonify({"plate_number": res}), 200
    except InvalidImage:
        logging.error("Invalid image")
        return jsonify({"error": "Invalid image"}), 400


# <url>:8080/idToNum?pict_ids=['123', '456']
# <url>:8080 : body: {"pict_ids": ['123', '456']}
# -> {
#   "plate_numbers": [
#     {
#       "pict_id": "10022",
#       "plate_number": "с181мв190"
#     },
#     {
#       "pict_id": "9965",
#       "plate_number": "о101но750"
#     }
#   ]
# }
@app.post("/idToNumBatch")
@error_handler
def id_to_number_batch():
    data = request.json.get("pict_ids", [])

    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid pict_ids data format"}), 400

    result = []

    for pict_id in data:
        im_data = image_provider_client.get_image(pict_id)

        if im_data is None:
            result.append(
                {
                    "pict_id": pict_id,
                    "error": f"Failed to fetch image for pict_id {pict_id}",
                }
            )
            continue

        im = io.BytesIO(im_data)
        try:
            res = plate_reader.read_text(im)
            result.append({"pict_id": pict_id, "plate_number": res})
        except InvalidImage:
            result.append({"pict_id": pict_id, "error": "Invalid image"})

    return jsonify({"plate_numbers": result}), 200


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(levelname)s] [%(asctime)s] %(message)s",
        level=logging.INFO,
    )

    app.config["JSON_AS_ASCII"] = False
    app.run(host="0.0.0.0", port=8080, debug=True)
