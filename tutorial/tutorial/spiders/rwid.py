import scrapy


class RwidSpider(scrapy.Spider):
    name = 'rwid'

    # jika domain direct ke web lain maka akan di reject
    allowed_domains = ['127.0.0.1']

    # mulai dari url ini
    start_urls = ['http://127.0.0.1:5000/']

    def parse(self, response):
        data = {
            'username': 'user',
            'password': 'user12345'
        }
        return scrapy.FormRequest(
            url='http://127.0.0.1:5000/login',
            formdata=data,
            callback=self.after_login
        )

    def after_login(self, response):
        """
        ada dua task disini
        1. ambil semua data barang yang ada di halaman hasil -> akan menuju detail (parsing detail)
        2. ambil semua link next -> akan kembali ke self.after_login
        """

        # task 1. get deatil products
        detail_prodicts = response.css(".card .card-title a")
        for i in detail_prodicts:
            link = i.attrib.get('href')
            yield response.follow(link, callback=self.parse_detail)

        # task 2. get next link
        pagination = response.css(".pagination a.page-link")
        for i in pagination:
            link = i.attrib.get('href')
            yield response.follow(link, callback=self.after_login)

        yield {"title": response.css("title::text").get()}

    def parse_detail(self, response):
        image = response.css(".card-img-top").attrib.get("src")
        title = response.css(".card-title::text").get()
        stock = response.css(".card-stock::text").get()
        desc = response.css(".card-text::text").get()

        return {
            'image': image,
            'title': title,
            'stock': stock,
            'desc': desc
        }


"""
untuk menampilkan file kedalam json atau csv:
scrapy crawl rwid -o data.json
scrapy crawl rwid -o data.csv
"""
