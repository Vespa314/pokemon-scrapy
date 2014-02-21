from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.conf import settings
import time
import sys
class Pokemon(BaseSpider):
    name = "Pokemon"
    f = open('pokemon_base_info.txt','wb');
    f_image = open('pokemon_image.txt','wb');
    start_urls = ["http://www.pokemon.name/wiki/%E7%B2%BE%E7%81%B5%E5%88%97%E8%A1%A8"];
    download_delay = 1
    def parse(self, response):
        reload(sys)                         # 2
        sys.setdefaultencoding('utf-8')     # 3
        req = []
        hxs = HtmlXPathSelector(response)
        PokemonNumbers = hxs.select("//tr/td[1]/text()").extract()
        PokemonNames = hxs.select("//tr/td[2]/a/text()").extract()
        PokemonLinks = hxs.select("//tr/td[2]/a/@href").extract()
        PokemonNumbers = PokemonNumbers[4:];
        PokemonNames = PokemonNames[1:];
        PokemonLinks = PokemonLinks[3:];
        for i in range(1,len(PokemonNumbers)):
            self.f.write(PokemonNumbers[i])
            self.f.write(':')
            self.f.write(PokemonNames[i])
            self.f.write(':')
            PokemonLinks[i] = 'http://www.pokemon.name'+PokemonLinks[i]
            self.f.write(PokemonLinks[i])
            self.f.write('\r\n')
            r = Request(PokemonLinks[i], callback=self.parse_GetPokemon_Detail)
            req.append(r)
        return req
        
    def parse_GetPokemon_Detail(self, response): 
        reload(sys)                         # 2
        sys.setdefaultencoding('utf-8')     # 3
        req = []
        hxs = HtmlXPathSelector(response)
        image = hxs.select("//table[1]/tr/td[1]/img[1]/@src").extract()
        name = hxs.select("//table/tr/th/div[3]/text()").extract()
        shuxing = hxs.select("//table/tr/td/a[@href='/wiki/%E5%B1%9E%E6%80%A7']/parent::*/following-sibling::*/a/text()").extract();
        id = hxs.select("//table/tr/td/a[@href='/wiki/%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4']/parent::*/following-sibling::*/b/text()").extract()
        heigth = hxs.select("//table/tr/td/a[@href='/wiki/%E8%BA%AB%E9%AB%98']/parent::*/following-sibling::*/text()").extract();
        weigth = hxs.select("//table/tr/td/a[@href='/wiki/%E4%BD%93%E9%87%8D']/parent::*/following-sibling::*/text()").extract();
        feacture = hxs.select("//table/tr/td/a[@href='/wiki/%E7%89%B9%E6%80%A7']/parent::*/following-sibling::*/a/text()").extract();
        hide_feacture = hxs.select("//table/tr/td/a[@href='/wiki/%E9%9A%90%E8%97%8F%E7%89%B9%E6%80%A7']/parent::*/following-sibling::*//text()").extract();
        gender = hxs.select("//table/tr/td/a[@href='/wiki/%E6%80%A7%E5%88%AB']/parent::*/following-sibling::*/text()").extract();
        power_idx = hxs.select("//h3/span[@id='.E7.A7.8D.E6.97.8F.E5.80.BC']/parent::*/following-sibling::*//dd//td[1]/text()").extract()
        
        zhaoshi = hxs.select("//table[@style='text-align:center;float:left;white-space:nowrap;margin:auto 0.2em 0.2em auto'][1]/tr").extract();
        
        
        print '-----------------------------',name[0],'------------------------'
        self.f_image.write(name[0])
        self.f_image.write("\r\nID:")
        self.f_image.write(id[0])
        self.f_image.write("\r\nAttribution:")
        for i in range(len(shuxing)):
            self.f_image.write(shuxing[i])
            self.f_image.write(' ')
        
        self.f_image.write('\r\nHP:')
        self.f_image.write(power_idx[0])
        self.f_image.write('Att:')
        self.f_image.write(power_idx[1])
        self.f_image.write('Def:')
        self.f_image.write(power_idx[2])
        self.f_image.write('Spe_Att:')
        self.f_image.write(power_idx[3])
        self.f_image.write('Spe_Def:')
        self.f_image.write(power_idx[4])
        self.f_image.write('Speech:')
        self.f_image.write(power_idx[5])
        self.f_image.write('Sum:')
        self.f_image.write(power_idx[6])
        
        self.f_image.write('Heigth:')
        self.f_image.write(heigth[0])
        self.f_image.write('\r\nWeigth:')
        self.f_image.write(weigth[0])
        self.f_image.write('\r\nFeacture:')
        self.f_image.write(feacture[0])
        self.f_image.write('\r\nHide_Feacture:')
        self.f_image.write(hide_feacture[0])
        self.f_image.write('\r\nGender rate:')
        self.f_image.write(gender[0])
        self.f_image.write('\r\n');
        self.f_image.write('Image Link:')
        self.f_image.write(image[0])
        for i in range(2,len(zhaoshi)+1):
            zs = hxs.select("//table[@style='text-align:center;float:left;white-space:nowrap;margin:auto 0.2em 0.2em auto'][1]/tr["+str(i)+"]/td//text()").extract()
            if(zs == []):
                break
            while(u'\n' in zs):
                zs.remove(u'\n')
            zs_name = hxs.select("//table[@style='text-align:center;float:left;white-space:nowrap;margin:auto 0.2em 0.2em auto'][1]/tr["+str(i)+"]/td/a/text()").extract()
            self.f_image.write(zs[0][:-1]+" ")
            self.f_image.write(zs_name[0]+" ")
            self.f_image.write(zs[2][:-1]+" ")
            self.f_image.write(zs[3][:-1]+" ")
            self.f_image.write(zs[4][:-1]+" ")
            self.f_image.write(zs[5][:-1]+"\r\n")

        self.f_image.write('\r\n\r\n')
        
        r = Request(image[0], callback=self.parse_GetPokemon_Image)
        req.append(r)
        return req
    def parse_GetPokemon_Image(self, response):
        str = response.url;
        str = str.split('/');
        imgfile = open(str[-1],'wb')
        imgfile.write(response.body)
        print '--------------image---------------',str[-1],'------------------------'