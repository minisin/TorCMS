# -*- coding:utf-8 -*-

import time

import peewee
from torcms.model.app2catalog_model import MApp2Catalog
from torcms.model.core_tab import CabMember
from torcms.model.ext_tab import TabUsage
from torcms.core import tools
from torcms.model.muser import MUser

class MUsage(object):
    def __init__(self):
        
        self.tab = TabUsage
        try:
            TabUsage.create_table()
        except:
            pass
        self.mapp2catalog = MApp2Catalog()
        self.muser = MUser()

    def get_all(self):
        return (self.tab.select().order_by('view_count'))

    def query_random(self):
        fn = peewee.fn
        return self.tab.select().order_by(fn.Random()).limit(6)

    def query_recent(self, uname, num):
        return self.tab.select().join(CabMember).where(CabMember.user_name == uname).order_by(self.tab.timestamp.desc()).limit(num)

    def query_recent_by_cat(self, uname, cat_id, num):
        return self.tab.select().join(CabMember).where( (self.tab.catalog_id == cat_id) &  (CabMember.user_name == uname)).order_by(self.tab.timestamp.desc()).limit(num)

    def query_most(self, uname, num):
        return self.tab.select().join(CabMember).where(CabMember.user_name == uname).order_by(self.tab.count.desc()).limit(num)

    def get_by_signature(self, u_name, sig):
        return self.tab.select().join(CabMember).where((self.tab.signature == sig) & (CabMember.uid == u_name))

    def count_increate(self, rec, cat_id, num):
        entry = self.tab.update(
            timestamp=int(time.time()),
            count= num + 1,
            catalog_id = cat_id,
        ).where(self.tab.uid == rec)
        entry.execute()

    def add_or_update(self, user_id, sig):
        tt =self.get_by_signature(user_id, sig)
        uu = self.mapp2catalog.get_entry_catalog(sig)
        if uu == False:
            return False
        cat_id = uu.catalog.uid
        if  tt.count() > 0:
            rec = tt.get()
            self.count_increate(rec.uid, cat_id, rec.count)
        else:
            entry = self.tab.create(
                uid=tools.get_uuid(),
                signature=sig,
                user= user_id,
                count=1,
                catalog_id =cat_id,
                timestamp=int(time.time()),
            )

