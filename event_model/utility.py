import uuid
from datetime import datetime
import pytz
import hashlib
import codecs


def make_timestamp():
    return datetime.now(pytz.utc).isoformat()


def make_uuid():
    return str(uuid.uuid4())


def uuid_convert(o):
    if isinstance(o, UUID):
        return str(o)


def compute_sha256(unicode_text):
    m = hashlib.sha256()
    m.update(unicode_text.encode("utf-8"))
    return m.hexdigest()


def file_sha256(filepath):
    # Read as Unicode, then re-encode as utf-8. Helps ensure canonical encoding.
    with codecs.open(filepath, "r", encoding="utf-8-sig") as f:
        m = hashlib.sha256()
        m.update(f.read().encode("utf-8"))
        return m.hexdigest()
