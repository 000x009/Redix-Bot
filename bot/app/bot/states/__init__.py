from .mailing import MailingSG
from .promo import EditPromoSG, InfoPromoSG, DeletePromoSG, CreatePromoSG
from .update_user import UpdateUserSG

"""SG stands for `States Group`"""

__all__ = [
    'MailingSG',
    'EditPromoSG',
    'InfoPromoSG',
    'DeletePromoSG',
    'CreatePromoSG',
    'UpdateUserSG',
]
