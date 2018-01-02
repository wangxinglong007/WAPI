# -*-coding:utf-8-*-
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class Pagination(object):

    def __init__(self, total_count, current_page, page_url, per_page_item_num=15, max_page_num=12):
        """
        :param total_count:         Total data     
        :param current_page:        current page
        :param per_page_item_num:   Number of pages per page
        :param max_page_num:        Display the maximum number of pages
        """
        # 数据总个数
        self.total_count = total_count
        # 当前页
        try:
            v = int(current_page)
            if v <= 0:
               v = 1
            self.current_page = v
        except Exception as e:
            self.current_page = 1
        # 每页显示的行数
        self.per_page_item_num = per_page_item_num
        # 最多显示页面
        self.max_page_num = max_page_num
        self.page_url = page_url

    def start(self):
        return (self.current_page-1) * self.per_page_item_num

    def end(self):
        return self.current_page * self.per_page_item_num

    @property
    def num_pages(self):

        a, b = divmod(self.total_count, self.per_page_item_num)
        if b == 0:
            return a
        return a+1

    def pager_num_range(self):

        if self.num_pages < self.max_page_num:
            return range(1, self.num_pages+1)
        # 总页数特别多 5
        part = int(self.max_page_num/2)
        if self.current_page <= part:
            return range(1, self.max_page_num+1)
        if (self.current_page + part) > self.num_pages:
            return range(self.num_pages-self.max_page_num+1, self.num_pages+1)
        return range(self.current_page-part, self.current_page+part+1)

    def page_str(self):

        page_list = []

        first = "<li><a href='/log?p=1%s'>首页</a></li>" % self.page_url
        page_list.append(first)

        if self.current_page == 1:
            prev = "<li><a href='#'>上一页</a></li>"
        else:
            prev = "<li><a href='/log?p=%s%s'>上一页</a></li>" % (self.current_page-1, self.page_url)
        page_list.append(prev)
        for i in self.pager_num_range():
            if i == self.current_page:
                temp = "<li class='active'><a href='/log?p=%s%s'>%s</a></li>" % (i, self.page_url, i)
            else:
                temp = "<li><a href='/log?p=%s%s'>%s</a></li>" % (i, self.page_url, i)
            page_list.append(temp)

        if self.current_page == self.num_pages:
            nex = "<li><a href='#'>下一页</a></li>"
        else:
            nex = "<li><a href='/log?p=%s%s'>下一页</a></li>" % (self.current_page + 1, self.page_url)
        page_list.append(nex)

        last = "<li><a href='/log?p=%s%s'>尾页</a></li>" % (self.num_pages, self.page_url)
        page_list.append(last)
        page_msg = '<span>第%s页/共%s页，合计%s条数据</span>' % (self.current_page, self.num_pages, self.total_count)
        page_list.append(page_msg)
        return ''.join(page_list)
