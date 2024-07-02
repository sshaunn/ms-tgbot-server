from datetime import datetime
import json


class Customer:
    uid: str
    firstname: str
    lastname: str
    tgid: str
    register_time: datetime = None
    is_member: bool = False
    is_whitelist: bool = False
    is_ban: bool = False
    join_time: datetime = None
    left_time: datetime = None

    def __init__(self, uid, firstname, lastname, tgid, register_time, is_member=False, is_whitelist=False, is_ban=False,
                 join_time=None, left_time=None):
        self.uid = uid
        self.firstname = firstname
        self.lastname = lastname
        self.tgid = tgid
        self.register_time = register_time
        self.is_member = is_member
        self.is_whitelist = is_whitelist
        self.is_ban = is_ban
        self.join_time = join_time
        self.left_time = left_time

    def set_membership(self, is_member):
        self.is_member = is_member

    def set_whitelist(self, is_whitelist):
        self.is_whitelist = is_whitelist

    # def format_date(self, date):
    #     self.date =

    def to_dict(self):
        return {
            'uid': self.uid,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'tgid': self.tgid,
            'register_time': self.register_time.strftime('%Y-%m-%d') if self.register_time else None,
            'is_member': self.is_member,
            'is_whitelist': self.is_whitelist,
            'is_ban': self.is_ban,
            'join_time': self.join_time.strftime('%Y-%m-%d') if self.join_time else None,
            'left_time': self.left_time.strftime('%Y-%m-%d') if self.left_time else None
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            uid=data['uid'],
            firstname=data['firstname'],
            lastname=data['lastname'],
            tgid=data['tgid'],
            register_time=data['register_time'].strftime('%Y-%m-%d') if data['register_time'] else None,
            is_member=data['is_member'],
            is_whitelist=data['is_whitelist'],
            is_ban=data['is_ban'],
            join_time=data['join_time'].strftime('%Y-%m-%d') if data['join_time'] else None,
            left_time=data['left_time'].strftime('%Y-%m-%d') if data['left_time'] else None
        )

    def to_json(self):
        return json.dumps(self.to_dict())
