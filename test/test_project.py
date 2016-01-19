
from os.path import abspath, dirname, join
current_path = abspath(dirname(__file__))
import sys
sys.path.insert(0, join(current_path, '..', "scloud"))
# sys.path.insert(0, join(current_path, '..'))
from scloud.config import logger
from scloud.async_services.listener import init_listener
from scloud.models.base import DataBaseService
from scloud.models.project import Pro_Info

init_listener()


if __name__ == '__main__':
    import uuid
    logger.info("-----[0 post_act_history]------")
    # try:
    with DataBaseService({}) as svc:
        proj = Pro_Info()
        proj.name = unicode(uuid.uuid4())
        proj.env_id = 1
        proj.user_id = 0
        proj.desc = u"123123"
        svc.db.add(proj)