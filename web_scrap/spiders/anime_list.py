import scrapy
import json

filename = "anime.json"  # To save store data
# filename = "sample.json"  # To save store data

class IntroSpider(scrapy.Spider):
    name = "anime_spider"
    def start_requests(self):
        s = ['winter', 'spring', 'summer', 'fall']

        urls = [
            'https://myanimelist.net/anime/season/{year}/{season}'.format(year=year, season=season) 
            for year in range(1990, 2023) for season in s
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def proc_img(self, img):
        k = img.split(' ')
        for i in k:
            if 'src' in i and 'srcset' not in i:
                return i.split('=')[1][1:-1]
    
    def parse(self, response):
        list_data=[]
        anime_link = response.css(
            'a.link-title::attr(href)'
        ).extract()

        anime_name = response.css(
            'a.link-title::text'
        ).extract()
        
        anime_rating = response.css(
            'span.js-score::text'
        ).extract()
        
        anime_sinopsis = response.css(
            'p.preline::text'
        ).extract()
        
        anime_genre = response.css(
            '.genres-inner'
        )
        
        anime_img = response.css(
            'div.image a img'
        ).getall()

        i=0
        for name in anime_name:
            data={
                'judul':name,
                'sinopsis':anime_sinopsis[i],
                'link':anime_link[i],
                'rating':anime_rating[i],
                'genre':[ x for x in anime_genre[i].css('a::text').extract()],
                'img':self.proc_img(anime_img[i]),
            }
            i+=1
            list_data.append(data)
            
        with open(filename, 'a+') as f:   # Writing data in the file
            for data in list_data : 
                app_json = json.dumps(data)
                f.write(app_json+"\n")