from datetime import datetime
from fastapi.encoders import jsonable_encoder

def CustomJSONEncoder(obj):
    def encode_datetime(obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        elif isinstance(obj, dict):
            return {k: encode_datetime(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [encode_datetime(item) for item in obj]
        return obj

    encoded = jsonable_encoder(obj)
    return encode_datetime(encoded)
    