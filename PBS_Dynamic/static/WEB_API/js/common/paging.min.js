(function(d, c, a) {
    function b(f, e) {
        this.el = f;
        this.options = { pageNo: e.initPageNo || 1, totalPages: e.totalPages || 1, totalCount: e.totalCount || "", slideSpeed: e.slideSpeed || 0, jump: e.jump || false, callback: e.callback || function() {} };
        this.init()
    }
    b.prototype = {
        constructor: b,
        init: function() {
            this.createDom();
            this.bindEvents()
        },
        createDom: function() {
            var k = this,
                m = "",
                e = "",
                j = "",
                g = 60,
                h = k.options.totalPages,
                l = 0;
            h > 5 ? l = 5 * g : l = h * g;
            for (var f = 1; f <= k.options.totalPages; f++) { f != 1 ? m += "<li>" + f + "</li>" : m += '<li class="sel-page">' + f + "</li>" }
            k.options.jump ? e = '<input type="text" placeholder="1" class="jump-text" id="jumpText"><button type="button" class="jump-button" id="jumpBtn">跳转</button>' : e = "";
            j = '<button type="button" id="firstPage" class="turnPage first-page">首页</button>' + '<button class="turnPage" id="prePage">上一页</button>' + '<div class="pageWrap" style="width:' + l + 'px">' + '<ul id="pageSelect" style="transition:all ' + k.options.slideSpeed + 'ms">' + m + "</ul></div>" + '<button class="turnPage" id="nextPage">下一页</button>' + '<button type="button" id="lastPage" class="last-page">尾页</button>' + e + '<p class="total-pages">共&nbsp;' + k.options.totalPages + "&nbsp;页</p>" + '<p class="total-count">' + k.options.totalCount + "</p>";
            k.el.html(j)
        },
        bindEvents: function() {
            var k = this,
                f = d("#pageSelect"),
                r = f.children(),
                n = r[0].offsetWidth,
                l = k.options.totalPages,
                g = k.options.pageNo,
                e = 0,
                o = d("#prePage"),
                m = d("#nextPage"),
                i = d("#firstPage"),
                j = d("#lastPage"),
                q = d("#jumpBtn"),
                h = d("#jumpText");
            o.on("click", function() {
                g--;
                if (g < 1) { g = 1 }
                p(g)
            });
            m.on("click", function() {
                g++;
                if (g > r.length) { g = r.length }
                p(g)
            });
            i.on("click", function() {
                g = 1;
                p(g)
            });
            j.on("click", function() {
                g = l;
                p(g)
            });
            q.on("click", function() {
                var s = parseInt(h.val().replace(/\D/g, ""));
                if (s && s >= 1 && s <= l) {
                    g = s;
                    p(g);
                    h.val(s)
                }
            });
            r.on("click", function() {
                g = d(this).index() + 1;
                p(g)
            });

            function p(s) {
                r.removeClass("sel-page").eq(s - 1).addClass("sel-page");
                if (l <= 5) { k.options.callback(s); return false }
                if (s >= 3 && s <= l - 2) { e = (s - 3) * n }
                if (s == 2 || s == 1) { e = 0 }
                if (s > l - 2) { e = (l - 5) * n }
                f.css("transform", "translateX(" + (-e) + "px)");
                s == 1 ? i.attr("disabled", true) : i.attr("disabled", false);
                s == 1 ? o.attr("disabled", true) : o.attr("disabled", false);
                s == l ? j.attr("disabled", true) : j.attr("disabled", false);
                s == l ? m.attr("disabled", true) : m.attr("disabled", false);
                k.options.callback(s)
            }
            p(k.options.pageNo)
        }
    };
    d.fn.paging = function(e) { return new b(d(this), e) }
})(jQuery, window, document);