import scrapy


class RacketSpider(scrapy.Spider):
    name = 'racket'
    start_urls = ['https://www.prospin.com.br/raquetes/tenis']

    def parse(self, response):
        for products, prices in zip(response.css('strong.product.name.product-item-name.-default'), 
                                    response.css('div.promocao-preco-avista')):
            yield {
                'name': products.css('a.product-item-link::text').get(),
                'price': prices.css('strong::text').get().replace('R$', '').replace(' ', ''),
                'link': products.css('a.product-item-link').attrib['href'],
            }

        next_page = response.css('a.action.next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)