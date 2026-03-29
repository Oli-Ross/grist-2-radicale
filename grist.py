from grist_api import GristDocAPI
from events import Event


from env import GRIST_URL, GRIST_DOC_ID, GRIST_TABLE


def get_events():
    api = GristDocAPI(GRIST_DOC_ID, server=GRIST_URL)
    data = api.fetch_table(GRIST_TABLE)
    return [Event.from_grist(x) for x in data]
