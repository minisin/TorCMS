# -*- coding:utf-8 -*-

import tornado.escape
from torcms.model.app_model import MApp
from torcms.model.minforcatalog import MInforCatalog

import config
from torcms.core.base_handler import BaseHandler
from torcms.model.app2catalog_model import MApp2Catalog


class InforTagHandler(BaseHandler):
    '''
    List the infos by the slug of the catalog.
    '''

    def initialize(self):
        self.init()

        self.mequa = MApp()
        self.mtag = MInforCatalog()
        self.mapp2tag = MApp2Catalog()

    def get(self, url_str=''):
        if len(url_str.strip()) == 0:
            return False

        url_arr = self.parse_url(url_str)

        if len(url_arr) == 1:
            self.list(url_str)
        elif len(url_arr) == 2:
            self.list(url_arr[0], url_arr[1])

    def list(self, tag_slug, cur_p=''):
        '''
        根据 cat_handler.py 中的 def view_cat_new(self, cat_slug, cur_p = '')
        :param tag_slug:
        :return:
        '''
        if cur_p == '' or cur_p == '-1':
            current_page_number = 1
        else:
            current_page_number = int(cur_p)
        taginfo = self.mtag.get_by_slug(tag_slug)
        num_of_tag = self.mapp2tag.count_of_certain_catalog(taginfo.uid)
        page_num = int(num_of_tag / config.page_num) + 1
        print(page_num)
        tag_name = taginfo.name

        kwd = {
            'tag_name': tag_name,
            'tag_slug': tag_slug,

            'title': tag_name,
        }

        self.render('infor/tag/list.html',
                    tag_name=tag_name,
                    infos=self.mapp2tag.query_pager_by_slug(tag_slug, current_page_number),
                    unescape=tornado.escape.xhtml_unescape,
                    kwd=kwd,
                    pager=self.gen_pager_bootstrap(tag_slug, page_num, current_page_number),
                    userinfo=self.userinfo,
                    )

    def gen_pager_bootstrap(self, cat_slug, page_num, current):
        # cat_slug 分类
        # page_num 页面总数
        # current 当前页面
        if page_num == 1:
            return ''

        pager_shouye = '''
        <li class=" {0}">
        <a  href="/tag/{1}">&lt;&lt; 首页</a>
                    </li>'''.format('hidden' if current <= 1 else '', cat_slug)

        pager_pre = '''
                    <li class=" {0}">
                    <a  href="/tag/{1}/{2}">&lt; 前页</a>
                    </li>
                    '''.format('hidden' if current <= 1 else '', cat_slug, current - 1)
        pager_mid = ''
        for ind in range(0, page_num):
            tmp_mid = '''
                    <li class="{0}">
                    <a  href="/tag/{1}/{2}">{2}</a></li>
                    '''.format('active' if ind + 1 == current else '', cat_slug, ind + 1)
            pager_mid += tmp_mid
        pager_next = '''
                    <li class=" {0}">
                    <a  href="/tag/{1}/{2}">后页 &gt;</a>
                    </li>
                    '''.format('hidden' if current >= page_num else '', cat_slug, current + 1)
        pager_last = '''
                    <li class=" {0}">
                    <a  href="/tag/{1}/{2}">末页
                        &gt;&gt;</a>
                    </li>
                    '''.format('hidden' if current >= page_num else '', cat_slug, page_num)
        pager = pager_shouye + pager_pre + pager_mid + pager_next + pager_last
        return (pager)

    def gen_pager(self, cat_slug, page_num, current):
        # cat_slug 分类
        # page_num 页面总数
        # current 当前页面
        if page_num == 1:
            return ''

        pager_shouye = '''
        <li class="pure-menu-item first {0}">
        <a class="pure-menu-link" href="/tag/{1}">&lt;&lt; 首页</a>
                    </li>'''.format('hidden' if current <= 1 else '', cat_slug)

        pager_pre = '''
                    <li class="pure-menu-item previous {0}">
                    <a class="pure-menu-link" href="/tag/{1}/{2}">&lt; 前页</a>
                    </li>
                    '''.format('hidden' if current <= 1 else '', cat_slug, current - 1)
        pager_mid = ''
        for ind in range(0, page_num):
            tmp_mid = '''
                    <li class="pure-menu-item page {0}">
                    <a class="pure-menu-link" href="/tag/{1}/{2}">{2}</a></li>
                    '''.format('selected' if ind + 1 == current else '', cat_slug, ind + 1)
            pager_mid += tmp_mid
        pager_next = '''
                    <li class="pure-menu-item next {0}">
                    <a class="pure-menu-link" href="/tag/{1}/{2}">后页 &gt;</a>
                    </li>
                    '''.format('hidden' if current >= page_num else '', cat_slug, current + 1)
        pager_last = '''
                    <li class="pure-menu-item last {0}">
                    <a class="pure-menu-link" href="/tag/{1}/{2}">末页
                        &gt;&gt;</a>
                    </li>
                    '''.format('hidden' if current >= page_num else '', cat_slug, page_num)
        pager = pager_shouye + pager_pre + pager_mid + pager_next + pager_last
        return (pager)
