from app.models import User
from app.utils import database_util as db_util
from app.utils.constants import MAX_GRAPHS_PER_USER


def is_user_able_to_create_graph(user_id):
    user = db_util.get_data_from_db_or_404(User, user_id)
    return user.graphs.count() <= MAX_GRAPHS_PER_USER
