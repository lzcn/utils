"""Create simple html file."""
import dominate
import dominate.tags as htags
import os


class SimpleHtml:
    """Simple html file contains concise elements."""

    def __init__(self, web_dir, title, reflesh=0):
        """Create a html file with concise elements."""
        # the title of SimpleHtml
        self.title = title
        # dir to save the web page
        self.web_dir = web_dir
        # dir to save the images
        self.img_dir = os.path.join(self.web_dir, 'images')
        if not os.path.exists(self.web_dir):
            os.makedirs(self.web_dir)
        if not os.path.exists(self.img_dir):
            os.makedirs(self.img_dir)
        # create a document with given title
        self.doc = dominate.document(title=title)
        # a time interval for the document to refresh itself
        if reflesh > 0:
            with self.doc.head:
                htags.meta(http_equiv="reflesh", content=str(reflesh))

    def add_header(self, str):
        """Add h3 header."""
        self.doc.add(htags.h3(str))
        return self.doc

    def add_table(self, border=1):
        """Add table."""
        table = htags.table(border=border, style="table-layout: fixed;")
        self.doc.add(table)
        return table

    def add_images(self, ims, txts, links, width=400):
        """Add images to table."""
        table = self.add_table()
        tr = table.add(htags.tr())
        with tr:
            for im, txt, link in zip(ims, txts, links):
                with htags.td(
                        style="word-wrap: break-word;",
                        halign="center",
                        valign="top"):
                    with htags.p():
                        with htags.a(href=os.path.join('images', link)):
                            htags.img(
                                style="width:%dpx" % width,
                                src=os.path.join('images', im))
                        htags.br()
                        htags.p(txt)

    def save(self):
        """Save html file."""
        html_file = '%s/index.html' % self.web_dir
        f = open(html_file, 'wt')
        f.write(self.doc.render())
        f.close()


if __name__ == '__main__':
    html = SimpleHtml('web/', 'test_html')
    html.add_header('hello world')

    ims = []
    txts = []
    links = []
    for n in range(4):
        ims.append('image_%d.png' % n)
        txts.append('text_%d' % n)
        links.append('image_%d.png' % n)
    html.add_images(ims, txts, links)
    html.save()
